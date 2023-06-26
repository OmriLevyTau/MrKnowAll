ENABLE_AUTH = True

SPLIT_METHOD= "nltk"
# SPLIT_METHOD = "hand"
# TEXT_EXTRACTION_METHOD = "PyPDF2"
TEXT_EXTRACTION_METHOD = "fitz"
EMBEDDING_MODEL="sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
ENABLE_EMBEDDING_MULTIPROC = False
# EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"

PINECONE_BATCH_SIZE = 100

# max number of tokens we can send to openAI API
MAX_NUM_OF_CHARS_IN_QUERY = 16000

# max number of chars we allow to user for asking a question
MAX_NUM_OF_CHARS_IN_QUESTION = 512

# Sbert has a limit of 128 words max
MAX_NUM_OF_WORDS_IN_QUERY = 128

# the threshold for the vectors score when we send a query
DEFAULT_SIMILARITY_SCORE_THRESHOLD = 0.3
DEFAULT_OPEN_AI_TEMPERATURE=0.0
DEFAULT_CONTEXT_WINDOW = 8
DEFAULT_TOP_K_VECTORS = 4
DEFAULT_OPENAI_GPT_MODEL = "gpt-3.5-turbo-16k"
