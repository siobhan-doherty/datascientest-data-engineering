from kafka import KafkaConsumer, TopicPartition


def decode_str(string):
    return None if string is None else string.decode("utf-8")

# basic decoding consumer
basic = KafkaConsumer(
    "test",
    bootstrap_servers=[
        "3.255.181.220:9092",
        "3.255.181.220:9093",
        "3.255.181.220:9094"
    ],
    auto_offset_reset="earliest",
    key_deserializer=decode_str,
    value_deserializer=decode_str,
    consumer_timeout_ms=500
)
print("=== BASIC ===")
for msg in basic:
    print(msg.key, msg.value)
basic.close()

# manual commit
manual = KafkaConsumer(
    "test",
    bootstrap_servers=[
        "3.255.181.220:9092",
        "3.255.181.220:9093",
        "3.255.181.220:9094"
    ],
    group_id="grp-manual",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    key_deserializer=decode_str,
    value_deserializer=decode_str,
    consumer_timeout_ms=500
)
print("\n=== MANUAL COMMIT ===")
for msg in manual:
    print(msg.key, msg.value)
    manual.commit()
manual.close()

# auto commit (only new messages)
auto = KafkaConsumer(
    "test",
    bootstrap_servers=[
        "3.255.181.220:9092",
        "3.255.181.220:9093",
        "3.255.181.220:9094"
    ],
    group_id="grp-auto",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    key_deserializer=decode_str,
    value_deserializer=decode_str,
    consumer_timeout_ms=500
)
print("\n=== AUTO COMMIT ===")
for msg in auto:
    print(msg.key, msg.value)
auto.close()

# assign to partition 0 only
pin = KafkaConsumer(
    bootstrap_servers=[
        "3.255.181.220:9092",
        "3.255.181.220:9093",
        "3.255.181.220:9094"
    ],
    group_id="grp-part0",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    key_deserializer=decode_str,
    value_deserializer=decode_str,
    consumer_timeout_ms=500
)
topic_partition_zero = TopicPartition("test", 0)
pin.assign([topic_partition_zero])
print("\n=== PARTITION 0 ONLY ===")
for msg in pin:
    print(msg.key, msg.value)
    pin.commit()
pin.close()

