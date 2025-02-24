from celery import shared_task, group, chain, chord

from django.apps import apps
from .utils import extract_text, get_no_of_pages

from itertools import islice

import logging

logger = logging.getLogger(__name__)

def chunk_list(lst, chunk_size):
    """
    Splits a list into chunks using islice.
    """
    iterator = iter(lst)
    return iter(lambda: list(islice(iterator, chunk_size)), [])

@shared_task
def process_pdf_task(document_id):
    """
    A Celery task to trigger pdf processing workflow.
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
