import os
import collections
import logging

import json
import tarfile
import io
import pickle as pkl


UTR_SPLITTER = '|'

logger = logging.getLogger()


def init_logger(log_file=None, log_file_level=logging.NOTSET):
    log_format = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    if log_file and log_file != '':
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger


def write_to_tar(dial_file, sum_file, out_file, makevocab=False, min_src_len=0, min_sum_len=0):
    """Reads the tokenized dialogue file and summary file writes them as the story and abstract to a out_file.
    """
    logger.info("Making bin file for {} and {}...".format(dial_file, sum_file))

    if makevocab:
        vocab_counter = collections.Counter()

    dial_lines = open(dial_file, encoding='utf-8').readlines()
    sum_lines = open(sum_file, encoding='utf-8').readlines()
    assert len(dial_lines) == len(sum_lines), "The number of dialogues should be the same with the number of the summaries."
    num_stories = len(dial_lines)

    logger.info("Total number of data: {}".format(num_stories))

    with tarfile.open(out_file, 'w') as writer:
        idx = -1
        for dial, summ in zip(dial_lines, sum_lines):
            # filter the data sample whose dialogue length is less than min_src_len
            if min_src_len > 0 and len(dial.strip().split()) < min_src_len:
                continue
            # filter the data sample whose summary length is less than min_sum_len
            if min_sum_len > 0 and len(summ.strip().split()) < min_sum_len:
                continue

            idx = idx + 1
            if idx % 1000 == 0:
                logger.info("Writing story {} of {}; {:.2f} percent done".format(
                    idx, num_stories, float(idx)*100.0/float(num_stories)))

            # Get the strings to write to .bin file
            # article_sents, abstract_sents = get_art_abs(story_file)
            article_sents = [line.strip() for line in dial.split(UTR_SPLITTER) if len(line.strip()) != 0]
            abstract_sents = [summ.strip()]

            # Write to JSON file
            js_example = {}
            js_example['id'] = idx
            js_example['article'] = article_sents
            js_example['abstract'] = abstract_sents
            js_serialized = json.dumps(js_example, indent=4).encode()
            save_file = io.BytesIO(js_serialized)
            tar_info = tarfile.TarInfo('{}/{}.json'.format(
                os.path.basename(out_file).replace('.tar', ''), idx))
            tar_info.size = len(js_serialized)
            writer.addfile(tar_info, save_file)

            # Write the vocab to file, if applicable
            if makevocab:
                art_tokens = ' '.join(article_sents).split()
                abs_tokens = ' '.join(abstract_sents).split()
                tokens = art_tokens + abs_tokens
                tokens = [t.strip() for t in tokens] # strip
                tokens = [t for t in tokens if t != ""] # remove empty
                vocab_counter.update(tokens)

    logger.info("Finished writing file {}\n".format(out_file))

    # write vocab to file
    if makevocab:
        logger.info("Writing vocab file...")
        with open(os.path.join(os.path.dirname(out_file), "vocab_cnt.pkl"),
                  'wb') as vocab_file:
            pkl.dump(vocab_counter, vocab_file)
        logger.info("Finished writing vocab file")

