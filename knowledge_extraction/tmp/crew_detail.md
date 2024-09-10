# System Description
The system is a data processing application that ingests, processes, and presents data. It uses a variety of technologies including Kafka, Spark, Cassandra, Hadoop, and REST APIs. The data flows from various sources, through a series of processing and storage components, and finally to a web/mobile application for user presentation.

# System Components
1. **Data Sources**: These are the initial sources of data for the system. They include market data, stock prices, and trades.
2. **Kafka Streaming Cluster**: This component handles real-time data streams from the data sources.
3. **Data Ingest (Spark Streaming)**: This component transforms, aggregates, and joins the data from the Kafka Streaming Cluster.
4. **Data Lake (Cassandra)**: This is a storage system for the processed data from the Spark Streaming component.
5. **Direct Data Push to App**: This component uses WebSocket/HTTP Streaming to send data from the Data Lake to the Web/Mobile App.
6. **Web/Mobile App**: These are the user interfaces that display the data. They use libraries like Bootstrap.js, Chart.js, and jQuery.js.
7. **Hadoop HDFS**: This is a distributed file system used for storage. It is connected to the Data Ingest (Spark Batch Processing) component.
8. **Data Ingest (Spark Batch Processing)**: This component is similar to Spark Streaming but is used for batch processing. It processes data from the Hadoop HDFS.
9. **REST API and Web Component**: This component facilitates interaction between the Web/Mobile App and the data services.

# Assets and Data Flow
- Data Sources -> Kafka Streaming Cluster: The data sources send data to the Kafka Streaming Cluster. The communication protocol is likely Kafka's native protocol.
- Kafka Streaming Cluster -> Data Ingest (Spark Streaming): The Kafka Streaming Cluster sends data to the Spark Streaming component. The communication protocol is likely Spark's native protocol.
- Data Ingest (Spark Streaming) -> Data Lake (Cassandra): The Spark Streaming component sends processed data to the Data Lake. The communication protocol is likely Cassandra's native protocol.
- Data Lake (Cassandra) -> Direct Data Push to App: The Data Lake sends data to the Direct Data Push to App component. The communication protocol is likely WebSocket/HTTP Streaming.
- Direct Data Push to App -> Web/Mobile App: The Direct Data Push to App component sends data to the Web/Mobile App. The communication protocol is likely WebSocket/HTTP Streaming.
- Hadoop HDFS -> Data Ingest (Spark Batch Processing): The Hadoop HDFS sends data to the Spark Batch Processing component. The communication protocol is likely Hadoop's native protocol.
- Data Ingest (Spark Batch Processing) -> Hadoop HDFS: The Spark Batch Processing component sends processed data back to the Hadoop HDFS. The communication protocol is likely Hadoop's native protocol.
- Web/Mobile App <-> REST API and Web Component: The Web/Mobile App interacts with the REST API and Web Component. The communication protocol is likely HTTP/HTTPS.
# Trust Boundaries:

- Data Sources: 1
- Kafka Streaming Cluster: 1
- Data Ingest (Spark Streaming): 4
- Data Lake (Cassandra): 8
- Direct Data Push to App: 2
- Web/Mobile App: 1
- Hadoop HDFS: 8
- Data Ingest (Spark Batch Processing): 4
- REST API and Web Component: 1
# Threat Scenarios:

1. External Hacker can exploit a vulnerability in the REST API and Web Component through SQL Injection to gain unauthorized access to sensitive data stored in the Data Lake (Cassandra). This scenario is classified as High severity.

2. Malicious Insider can perform a Man-in-the-Middle attack on the Kafka Streaming Cluster to intercept and manipulate data being transmitted between the Data Ingest (Spark Streaming) and Hadoop HDFS. This scenario is classified as Medium severity.

3. Phishing Attacker can send a malicious link to a user of the Web/Mobile App, leading to a Cross-Site Scripting (XSS) attack that compromises the user's session and allows unauthorized access to Direct Data Push to App. This scenario is classified as Medium severity.

4. Competitor can launch a Denial of Service (DoS) attack on the Data Ingest (Spark Batch Processing) component, causing a disruption in data processing and affecting the availability of the system. This scenario is classified as High severity.
- Controls

1. Countermeasure for Threat Scenario 1 (External Hacker exploiting SQL Injection):
   - Implement input validation and parameterized queries in the REST API to prevent SQL Injection attacks.
   - Regularly update and patch the Web Component to fix any known vulnerabilities.
   - Implement access controls and encryption mechanisms to protect sensitive data in the Data Lake.
   - Monitor and log all access to the Data Lake to detect any unauthorized activities.

2. Countermeasure for Threat Scenario 2 (Malicious Insider performing Man-in-the-Middle attack):
   - Implement end-to-end encryption between the Data Ingest and Hadoop HDFS to prevent data interception.
   - Use strong authentication mechanisms for accessing the Kafka Streaming Cluster.
   - Regularly monitor network traffic for any suspicious activities or anomalies.
   - Conduct regular security training for employees to raise awareness about insider threats.

3. Countermeasure for Threat Scenario 3 (Phishing Attacker launching XSS attack):
   - Implement input validation and output encoding in the Web/Mobile App to prevent XSS attacks.
   - Use HTTPS and secure cookies to protect user sessions from being compromised.
   - Implement email filtering and user awareness training to detect and prevent phishing attacks.
   - Regularly update and patch the Web/Mobile App to fix any security vulnerabilities.

4. Countermeasure for Threat Scenario 4 (Competitor launching DoS attack):
   - Implement rate limiting and traffic filtering mechanisms in the Data Ingest component to mitigate DoS attacks.
   - Use a Content Delivery Network (CDN) to distribute incoming traffic and reduce the impact of DoS attacks.
   - Implement DDoS protection services to detect and block malicious traffic.
   - Regularly test and optimize the system's capacity to handle high volumes of traffic to prevent service disruptions.
