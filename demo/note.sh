# 创建topic
kafka-topics.sh --create --topic kafka-test --replication-factor 1 --partitions 1 --bootstrap-server middleware-kafka.tink:9092

# 查看topic 列表
kafka-topics.sh --list --bootstrap-server middleware-kafka.tink:9092

# 查看 tipoc 详情
kafka-topics.sh --bootstrap-server  middleware-kafka.tink:9092 --topic jmeter-example --describe

# 消费
kafka-console-consumer.sh --bootstrap-server middleware-kafka.tink:9092 --topic jmeter-example --from-beginning

# 生产性能测试
kafka-consumer-perf-test.sh --topic jmx --broker-list middleware-kafka.tink:9092 --messages 1000






# minio
mc share download --json --expire 4h minio/jmx/abc |jq '.url' | xargs wget 

# 查看日志
kubectl get pod  -n tink | grep atop | awk '{print $1}' | xargs -n 1 -i{} kubectl logs {} -n tink -c filebeat

# 创建configMap
kubectl create configmap jmx-file --from-file=jmx=/example.jmx -n tink


kubectl get pod  -n tink | grep testing | awk '{print $1}' | xargs -n 1 -i{} kubectl exec -it {} -n tink -- bash