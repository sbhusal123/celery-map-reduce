# Map Reduce Workflow With Celery

Parallelizing Workflow With Group and Chords to achieve Map Reduce Workflow With Celery.

Starting a Celery Worker: ``celery -A src  worker --loglevel=info``

## Models:

**src/foo/models.py**

```python
class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='pdfs/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    pdf_text = models.TextField(blank=True)
    entities = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        m =  super().save(*args, **kwargs)
        return m

@receiver(post_save, sender=Document)
def trigger_send_email_task(sender, instance, created, **kwargs):
    """Whenever a new document is uploaded, triggers process task"""
    if created:
        process_pdf_task.delay(instance.id)

post_save.connect(trigger_send_email_task, sender=Document)
```

Whenever a object is created, pdf file is uploaded, it triggers ``process_pdf_task`` task.

## Tasks

```python
from itertools import islice

def chunk_list(lst, chunk_size):
    """
    Splits a list into chunks using islice.
    """
    iterator = iter(lst)
    return iter(lambda: list(islice(iterator, chunk_size)), [])

@shared_task
def process_pdf_task(document_id):
    """
    A Celery task to send an email to a user.
    This task is assigned to the 'high_priority' queue.
    """
    Document = apps.get_model("foo", "Document")
    document = Document.objects.get(id=document_id)

    page_count = get_no_of_pages(document.pdf_file.path)
    
    logger.info(f"Processing pdf ({document.pdf_file.name}) with page count: {page_count}")

    pages = list(range(1, page_count + 1))


    # We could have used chain, but we want combine_result to be called only once
    # after all the extract_text_from_pdf and extract_named_entities tasks are completed.
    task = chord(
        group(
            chain(
                extract_text_from_pdf.s(document_id, pages),
                extract_named_entities.s()
            ) for pages in chunk_list(pages, 2)
        ),
        combine_result.s(document_id)
    )
    

    # Execute all tasks in parallel
    result = task.apply_async()

    logger.info("Processing pdf")
    logger.info(f"\nresult::\n{result}")

    
    return document_id

@shared_task(queue="pdf_to_text")
def extract_text_from_pdf(document_id, pages):
    """
    Document id: The id of the document whose text needs to be extracted.
    pages: An array of page numbers to extract text from.
    """
    Document = apps.get_model("foo", "Document")
    document = Document.objects.get(id=document_id)
    
    text = extract_text(document.pdf_file.path, pages)

    logger.info(f"Extracting text from pdf: , {document.pdf_file.name}, Pages: , {pages}")
    logger.info(f"\n\ntext={text}\n\n")

    return {
        "text": text,
        "pages": pages
    }

@shared_task(queue="named_entity_extraction")
def extract_named_entities(result):
    """
    result: The result of the previous task.
    document_id: The id of the document whose named entities need to be extracted.
    """
    text = result["text"]
    pages = result["pages"]
    logger.info(f"Extracting entities from text: {text}")
    return {
        "entities": ["entity1", "entity2", "entity3"],
        "text": text,
        "pages": pages
    }


@shared_task
def combine_result(results, document_id):
    """
    results: The results of the previous tasks.
    document_id: The id of the document whose results need to be combined.
    """
    # preserved as in the order of page.
    sorted_results = sorted(results, key=lambda x: x["pages"][0])

    extracted_entities = []
    extracted_text = ""
    for result in sorted_results:
        extracted_entities.extend(result["entities"])
        extracted_text += result["text"]

    Document = apps.get_model("foo", "Document")
    document = Document.objects.get(id=document_id)
    document.pdf_text = extracted_text
    document.entities = extracted_entities
    document.save()
    
    logger.info(f"Finished Processing...")
    return {"combined_result": "result"}
```

Since, we are executing a task through some queues, if it needs to be scaled, it can be achieved using.

```sh
celery -A src worker --loglevel=info --concurrency=3 -Q pdf_to_text
```

This runs 3 workers in parallel for processing pdf to text.

```sh
celery -A src worker --loglevel=info --concurrency=3 -Q named_entity_extraction
```

This runs 3 workers in parallel for extracting named entities from text.

Refer [Starting Celery With Options](./Celery%20Commands.md) section for more.


## Workflow:

Workflow looks like below:

```python
task = chord(
    group(
        chain(
            extract_text_from_pdf.s(document_id, pages),
            extract_named_entities.s()
        ) for pages in chunk_list(pages, 2)
    ),
    combine_result.s(document_id)
)
```

```sh
        process_pdf
             |
      -------------------------
      |           |           |
 extract_text   extract_text  extract_text
   (1,2)         (3,4)        (5,6)
      |           |           |
 extract_entity  extract_entity extract_entity
   (1,2)         (3,4)        (5,6)
      |___________|___________|
             |
     combine_result

```

1. At first ``process_pdf`` task is triggered.

2. Internally, it chunks the no of pages into 2 pages, i.e. if 6 pages were there, on chunking it with 2 subscequent pages, we get a 3 group of 2 pages.

3. Those group of three task execute parallely. When a individual task (extract_pdf) is finished executing, with the return of extract_pdf task, it executes extract_entity task. **This is called chaining, i.e. runing task B after finishing task A.**

4. After finishing extract_entity task for all of the grouped task, all the result of the 2nd phase is passed to, combine_result task. This is where the results are reduced or combined.

**Altogether this can be thought of as a map reduce workflow:**
- 1st phase is where mapping happens.
- 4th phase is where reduce workflow is achieved.



## Commands:

- Create Superuser: ``make createsuperuser``

- Start NER worker: ``make start_ner_worker``

- Start Default Worker: ``make start_worker``

- Start PDF To Text Worker: ``make start_pdf_to_text_worker``

Note that:

- NER Worker listens on ``named_entity_extraction`` queue.

- Pdf to text Worker listens on ``pdf_to_text`` queue.



## References:

- [Starting Celery Worker, Options](./Celery%20Commands.md)

- [Understandnig group, chains and chords](./Group,%20Chain%20and%20Chords.md)
