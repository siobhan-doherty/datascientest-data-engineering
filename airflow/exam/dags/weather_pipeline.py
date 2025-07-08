from airflow import DAG
from airflow.models import Variable 
from airflow.utils.helpers import chain
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from joblib import dump
import datetime, os, json, requests, pandas as pd


RAW = "/app/raw_files"
CLEAN = "/app/clean_data"
API = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(**ctx):
    cities = Variable.get("cities", deserialize_json = True)
    key = Variable.get("api_key")
    raw_ts = ctx["ts"]
    time_stamp = raw_ts.replace(":", ".")
    destination = os.path.join(RAW, f"{time_stamp}.json")

    all_data = []
    for city in cities:
        try:
            response = requests.get(API, params = {"q": city, "appid": key}, timeout = 10)
            response.raise_for_status()  # HTTP errors -> exception
            data = response.json()  # JSON parse errors -> exception
        except requests.RequestException as e:
            logging.error(f"[fetch_weather] HTTP error for {city}: {e}")
            continue    # skip this city
        except ValueError as e:
            logging.error(f"[fetch_weather] JSON decode error for {city}: {e}")
            continue

        all_data.append(data)

    if not all_data:
        # no successful responses at all
        logging.warning("[fetch_weather] no city data fetched this run")
    else:
        with open(destination, "w") as f:
            json.dump(all_data, f)

    return destination

def transform_csv(n_files = None, filename = "data.csv"):
    files = sorted(os.listdir(RAW), reverse = True)
    if n_files:
        files = files[:n_files]
    rows = []
    for fn in files:
        data = json.load(open(os.path.join(RAW, fn)))
        time_stamp = fn.split(".")[0]
        for city in data:
            rows.append({
                "temperature": city["main"]["temp"],
                "city": city["name"],
                "pression": city["main"]["pressure"],
                "date": time_stamp
            })
    pd.DataFrame(rows).to_csv(os.path.join(CLEAN, filename), index = False)

def prepare_data(df: pd.DataFrame):
    df = df.sort_values(["city", "date"])
    dfs = []
    for city in df["city"].unique():
        sub = df[df["city"] == city].copy()
        sub["target"] = sub["temperature"].shift(1)
        for i in range(1, 10):
            sub[f"temp_m-{i}"] = sub["temperature"].shift(-i)
        dfs.append(sub.dropna())
    final = pd.concat(dfs, ignore_index = True).drop(["date"], axis = 1)
    final = pd.get_dummies(final, columns = ["city"])
    X = final.drop("target", axis = 1)
    y = final["target"]
    
    return X, y

def train_model(model_cls, **ctx):
    df = pd.read_csv(os.path.join(CLEAN, "fulldata.csv"))
    if len(df) < 3:
        # skip run if not enough samples
        return
    X, y = prepare_data(df)
    score = cross_val_score(model_cls(), X, y, 
                            cv = 3, scoring = "neg_mean_squared_error").mean()
    ctx["task_instance"].xcom_push(key = "score", value = float(score))
    dump(model_cls().fit(X, y), 
        f"/app/clean_data/{model_cls.__name__}.pkl")

def select_best(**ctx):
    task_instance = ctx["task_instance"]
    scores = {
        name: task_instance.xcom_pull(task_ids = f"train_{name}", key = "score")
        for name in ["linear_regression", "decision_tree", "random_forest"]
    }
    best = min(scores, key = scores.get)
    cls = {
        "linear_regression": LinearRegression, 
        "decision_tree": DecisionTreeRegressor, 
        "random_forest": RandomForestRegressor
    }[best]
    df = pd.read_csv(os.path.join(CLEAN, "fulldata.csv"))
    X, y = prepare_data(df)
    dump(cls().fit(X, y), os.path.join(CLEAN, "best_model.pkl"))

with DAG(
    dag_id = "weather_pipeline",
    default_args={
        "owner": "airflow",
        "start_date": datetime.datetime(2025, 7, 8)
    },
    schedule_interval = "* * * * *",  # every minute
    catchup = False
) as dag:
    start = EmptyOperator(task_id = "start")
    # fetch current weather for each city
    t1 = PythonOperator(
        task_id = "fetch_weather", 
        python_callable = fetch_weather
    )
    # last-20 files -> data.csv
    t2 = PythonOperator(
        task_id = "transform_recent", 
        python_callable = transform_csv, 
        op_kwargs = {"n_files": 20, "filename": "data.csv"}
    )
    # all files -> full_data.csv
    t3 = PythonOperator(
        task_id = "transform_all", 
        python_callable = transform_csv, 
        op_kwargs = {"n_files": None, "filename": "fulldata.csv"}
    )
    # train three different models
    trains = []
    for name, cls in [
        ("linear_regression", LinearRegression), 
        ("decision_tree", DecisionTreeRegressor),
        ("random_forest", RandomForestRegressor)
    ]:
        trains.append(
            PythonOperator(
                task_id = f"train_{name}", 
                python_callable = train_model, 
                op_kwargs = {"model_cls": cls}
            )
        )
    # pick the best model
    t5 = PythonOperator(
        task_id = "select_best", 
        python_callable = select_best
    )

    end = EmptyOperator(task_id = "end")
    # clean wire up: start -> fetch -> [transform_recent, transform_all] -> train -> select_best -> end
    chain(
        start,
        t1,
        [t2, t3],
        *trains,
        t5,
        end
    )
