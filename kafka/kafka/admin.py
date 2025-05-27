import argparse
from kafka.admin import KafkaAdminClient, NewTopic


admin = KafkaAdminClient(
    bootstrap_servers=[
      "3.255.181.220:9092",
      "3.255.181.220:9093",
      "3.255.181.220:9094"
    ],
    client_id="admin"
  )

def create_topic(name, partitions, replication):
    topic = NewTopic(
        name=name,
        num_partitions=partitions,
        replication_factor=replication
    )
    admin.create_topics([topic])
    print(f"Topic '{name}' created")

def delete_topic(name):
  admin.delete_topics([name])
  print(f"Topic '{name}' deleted")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Admin Kafka Topics")
  parser.add_argument("action", choices=["create", "delete"])
  parser.add_argument("-n","--name", required=True, help="Topic name")
  parser.add_argument("-p","--partitions", type=int, default=4)
  parser.add_argument("-r","--replication", type=int, default=3)
  args = parser.parse_args()

  if args.action == "create":
    create_topic(args.name, args.partitions, args.replication)
  else:
    delete_topic(args.name)

  admin.close()

