import base64

from google.cloud import storage


def write_to_gcs(data, context):
    # Messaggio Pub/Sub in formato application/octet-stream
    pubsub_message = base64.b64decode(data["data"]).decode(
        "utf-8"
    )  # Decodifica del messaggio

    # Estrai il nome del bucket e il file
    bucket_name = "solarcar_bucket"
    # Salva i messaggi come file unici con id evento
    file_name = f"messages/message-{context.event_id}.txt"

    # Crea il client per Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Scrivi il messaggio nel file di testo
    blob.upload_from_string(pubsub_message)

    print(f"Messaggio scritto nel bucket {bucket_name}, file {file_name}")
