# open-crawler

This is ScanR crawler application. It is a web crawler developped in python.
## Prerequisites

Make sure you have installed :

* git
* docker-compose
## Installation

Git clone project

```bash
  git clone https://github.com/dataesr/open-crawler.git
  cd open-crawler
```
    
## Environment Variables

To configure this project, you will need to change the following environment variables in your .env file

For RabbitMQ :

`RABBITMQ_USERNAME`

`RABBITMQ_PASSWORD`

For volumes mount:

`LOCAL_FILES_PATH`

`MINIO_PATH`

`MONGODB_PATH`

For storage service:

`HTML_FOLDER_NAME`

`METADATA_FOLDER_NAME`



## Deployment

To deploy this project run

```bash
  docker-compose up
```


## API Reference

#### Start a new crawl

```http
  POST http://127.0.0.1:8080/crawl
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. Starting url to crawl from |
| `depth` | `integer` | Maximum depth to crawl (**Default**: 2) |
| `limit` | `integer` | Maximum pages to crawl (**Default**: 50) |
| `headers` | `dict[str, str]` | Headers that will be passed to all crawl requests |
| `metadata` | `list[MetadataConfig]` | Metadata config overload |

**MetadataConfig**

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name` | `str` | Name of the metadata (accessibility, good_practices, technologies, responsiveness, carbon_footprint) |
| `enabled` | `boolean` | Should the metadata be processed |
| `depth` | `integer` | Maximum depth for which the metadata should be processed (sets enabled to true if not present)|



## Demo

![demo](./demo/demo.gif)

