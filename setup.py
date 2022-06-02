import os
import nltk


def download_nltk_shakespeare(download_dir):
    print(f"Ensuring that {download_dir} exists")
    os.makedirs(download_dir, exist_ok=True)

    print("Downloading shakespeare corpus")
    nltk.download("shakespeare", download_dir)
    nltk.data.path.append(download_dir)

    print("Extracting words from shakespeare corpus")
    words = []
    for book in nltk.corpus.shakespeare.fileids():
        words.extend(nltk.corpus.shakespeare.words(book))

    output_path = os.path.join(download_dir, "words.txt")
    print(f"Saving words at {output_path}")
    with open(output_path, "w") as f:
        f.write("\n".join(words))


def filter_k_letter_words(word_file_path, k=5, output_path=None):
    with open(word_file_path) as f:
        word_list = f.read().splitlines()
    filtered_word_list = [w for w in word_list if len(w) == k]

    output_path = os.path.join(os.path.dirname(
        word_file_path), f"{k}_lettered_words.txt") if output_path is None else output_path
    print(f"Saving {k} lettered words at {output_path}")
    with open(os.path.join(output_path), "w") as f:
        f.write("\n".join(filtered_word_list))


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    download_nltk_shakespeare(
        download_dir=os.path.join(ROOT_DIR, "data/nltk/"))
    filter_k_letter_words(word_file_path=os.path.join(
        ROOT_DIR, "data/nltk/words.txt"))
