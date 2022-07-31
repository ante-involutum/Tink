kafka-console-consumer.sh --bootstrap-server middleware-kafka.tink:9092 --topic jmx --from-beginning


kafka-topics.sh --create --topic kafka-test --replication-factor 1 --partitions 1 --bootstrap-server middleware-kafka.tink:9092



mc share download --json --expire 4h minio/jmx/abc |jq '.url' | xargs wget 


kafka-topics.sh --list --bootstrap-server middleware-kafka.tink:9092
kafka-console-consumer.sh --bootstrap-server middleware-kafka.tink:9092 --topic jmx --from-beginning

kafka-consumer-perf-test.sh --topic jmx --broker-list middleware-kafka.tink:9092 --messages 1000


watch -n 5  "kubectl get pod  -n tink | grep atop | awk '{print $1}' | xargs -n 1 -i{} kubectl logs {} -n tink -c filebeat "