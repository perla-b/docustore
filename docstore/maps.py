import enum
from docstore.models import Document, Folder, Topic

class dtypes(enum.Enum):
    folder = 'folders'
    doc = 'docs'
    topics = 'topics'

    def contains(val):
        items = list(dtypes)
        items = [v.value for v in items]
        return (val in items)

model_maps = {
    dtypes.folder.value : Folder,
    dtypes.doc.value : Document,
    dtypes.topics.value : Topic,
}