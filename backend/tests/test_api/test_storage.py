import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



@pytest.mark.asyncio
async def test_user_gets_all_documents_metadata():
    """_summary_
    1. Create an authenticated user
    2. Insert 3 documents and store aside their metadata.
    3. Call client.get(/documents) and store response
    4. Verify status==200 and that the response contains a list of 3 documents-metadata
    5. Assert all fields are correct
    6. Use the documents id to verify the VectorStorage store this documnets as well
    """
    pass

@pytest.mark.asyncio
async def test_different_users_get_their_documents_metadata():
    """_summary_
    should create two different authenticated users,
    each of whom will create 2 documnets.
    Then use a client for each user, verify each user
    get a list contains his/her two inserted documents
    and status code of 200.
    """
    pass

#######################
####### Uploads #######
#######################

@pytest.mark.asyncio
async def test_upload_document():
    """_summary_
    should create an authenticated user,
    then upload a document (client.post(/document)),
    then verify the status code (204) and hold the id
    given in the response. Then retrieve the document
    and verify the response equals the pre-defined document.
    """
    pass


@pytest.mark.asyncio
async def test_cannot_upload_no_document():
    """_summary_
    an authenticated user tries to upload but no pdf
    is attached. Should fail with 400 status code.
    """


@pytest.mark.asyncio
async def test_cannot_upload_non_pdf_document():
    """_summary_
    an authenticated user tries to upload non-pdf
    file. Should fail with status code of 400.
    """
    pass


#######################
###### Deletions ######
#######################

@pytest.mark.asyncio
async def test_delete_document():
    """_summary_
    an authenticated user creates a document and gets back
    its id. Then verify it is contained in the DB (get metadata).
    Then users delets this document, verify status code of 204
    and then tries to retrieve it again and get resonse of document
    not exist
    """
    pass

@pytest.mark.asyncio
async def test_cannot_delete_non_existing_document():
    """_summary_
    An authenticated user tries to delete non-existing document
    and failes with status code 400
    """

@pytest.mark.asyncio
async def test_user_cannot_delete_not_her_document():
    """_summary_
    should create two different authenticated users,
    first user upload a new document and keeps its ID.
    then second user tries to delete this document by id
    but will fail as it's not exists in its database.

    """
    pass

#######################
####### Retrieve ######
#######################

@pytest.mark.asyncio
async def test_get_document():
    pass

@pytest.mark.asyncio
async def test_user_cannot_get_non_existing_document():
    pass

@pytest.mark.asyncio
async def test_user_cannot_get_not_her_document():
    pass

@pytest.mark.asyncio
async def test_different_users_get_their_document():
    pass
