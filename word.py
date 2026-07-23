from docx import Document


class Word:
    @staticmethod
    def clear_document(doc_name):
        document = Document()
        document.save('word_documents/' + doc_name + '.docx')
        return document
