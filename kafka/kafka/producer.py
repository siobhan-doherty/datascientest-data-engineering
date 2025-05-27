from kafka import KafkaProducer


def encode_str(string):
  return None if string is None else string.encode("utf-8")
  
def decode_str(string):
  return None if string is None else string.decode("utf-8")

def custom_partitioner(key, all_partitions, available_partitions):
  # if no key, go to last partition
  if key is None:
    return all_partitions[-1]
  # else map to int
  return int(decode_str(key))

producer = KafkaProducer(
  bootstrap_servers=[
     "3.255.181.220:9092", 
     "3.255.181.220:9093", 
     "3.255.181.220:9094"
  ],
  client_id="easy_production",
  key_serializer=encode_str,
  value_serializer=encode_str,
  partitioner=custom_partitioner,
  acks='all', # wait for all replicas
  retries=5,  # try up to 5 attempts in failure scenario
)

for i in range(1, 6):
    producer.send("test", value=f"No need encoding # {i}")

for i in range(1, 30):
    producer.send(topic="test", value=f"New message # {i}", key=f"{i % 2}")

for i in range(30, 59):
    producer.send(topic="test", value=f"New message # {i}")

producer.flush()
producer.close()

