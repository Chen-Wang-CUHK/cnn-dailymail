import spacy
from spacy.tokenizer import Tokenizer

SENT_END_TOKENS = ['.', ',', '?', '!', ';']
COREF_TEXT_TOKEN_NUM_TH = 4

class SpacyNLP(object):
    def __init__(self, whitespace_tokenizer_for_coref=True, whitespace_tokenizer_for_tokenizer=False):
        # for tokenization
        self.tokenize_nlp = spacy.load('en')
        if whitespace_tokenizer_for_tokenizer:
            self.tokenize_nlp.tokenizer = Tokenizer(self.tokenize_nlp.vocab)

        # for coreference resolution
        self.whitespace_tokenizer_for_coref = whitespace_tokenizer_for_coref
        self.coref_nlp = spacy.load('en')
        if whitespace_tokenizer_for_coref:
            self.coref_nlp.tokenizer = Tokenizer(self.coref_nlp.vocab)
        # neuralcoref.add_to_pipe(self.coref_nlp)

    def word_tokenize(self, text):
        text = text.strip()
        doc = self.tokenize_nlp.tokenizer(text)
        token_list = [span.string.strip() for span in doc]
        return token_list

    def sent_tokenize(self, text, use_space_split_tokens_in_sent=False):
        text = text.strip()
        doc = self.tokenize_nlp(text)
        if use_space_split_tokens_in_sent:
            sents = [s.string.strip().split() for s in doc.sents]
        else:
            sents = [self.word_tokenize(s.string.strip()) for s in doc.sents]
        return sents

    # def neuralcoref(self, text):
    #     """
    #     neural corefernece function for the pre-tokenized text
    #     :param text: the source text input
    #     :return:
    #     """
    #     text = text.strip()
    #     doc = self.coref_nlp(text)
    #
    #     spacy_tokenized_words = [w.string.strip() for w in doc]
    #     reconstructed_text = ' '.join(spacy_tokenized_words)
    #     if self.whitespace_tokenizer_for_coref:
    #         assert reconstructed_text == text, "tokenized_dial: {} \n reconstructed from corefs: {}".format(text.split(' '), spacy_tokenized_words)
    #
    #     # pick out the represent_mention (i.e. the main mention) and the resoluted mention for each cluster
    #     coref_clusters = []
    #     resoluted_used_indicators = [0] * 10000
    #     for cluster in doc._.coref_clusters:
    #         reformed_mentions = {'m_text_list': [], 'm_posi_list': [], 'm_coref_scores_list': []}
    #         # the main mention is not always the first mention 'assert cluster[0] == cluster.main' will be false
    #         # but we put the main mention in the first position in reformed_mentions
    #         reformed_cluster = [cluster.main]
    #         for mention in cluster:
    #             if mention != cluster.main:
    #                 reformed_cluster.append(mention)
    #         assert len(cluster) == len(reformed_cluster)
    #
    #         filtered_cluster = []
    #         for mention in reformed_cluster:
    #             mention_text = mention.string.strip()
    #             # mention filter condition 1,
    #             # if the text contain sentence ending tokens
    #             if any([tok in mention_text for tok in SENT_END_TOKENS]):
    #                 # logger.info('Mention sent_end_token filter: ', mention_text, (mention.start, mention.end))
    #                 continue
    #             # mention filtering condition 2,
    #             # the length of the text is larger than COREF_TEXT_TOKEN_NUM_TH
    #             if len(mention_text.split()) > COREF_TEXT_TOKEN_NUM_TH:
    #                 # logger.info('Mention COREF_TEXT_TOKEN_NUM_TH filter: ', mention_text, (mention.start, mention.end))
    #                 continue
    #             # mention filtering condition 3
    #             # We filter out the overlapped corefs
    #             if sum(resoluted_used_indicators[mention.start: mention.end]) != 0:
    #                 # logger.info('Mention overlapping filter: ', mention_text, (mention.start, mention.end))
    #                 continue
    #
    #             resoluted_used_indicators[mention.start: mention.end] = [1] * (mention.end - mention.start)
    #             filtered_cluster.append(mention)
    #
    #         reformed_cluster = filtered_cluster
    #
    #         # cluster filter condition 1, if there is only one or zero mention
    #         if len(reformed_cluster) <= 1:
    #             continue
    #
    #         coref_scores = numpy.zeros((len(reformed_cluster), len(reformed_cluster)))
    #         for i in range(len(reformed_cluster)):
    #             mention = reformed_cluster[i]
    #             reformed_mentions['m_text_list'].append(mention.string.strip())
    #             reformed_mentions['m_posi_list'].append([mention.start, mention.end])
    #             # visited_mention_spans.append(mention)
    #             for j in range(len(reformed_cluster)):
    #                 visited_mention = reformed_cluster[j]
    #                 if visited_mention in mention._.coref_scores:
    #                     assert coref_scores[i][j] == 0.0
    #                     coref_scores[i][j] = round(mention._.coref_scores[visited_mention], 2)
    #                     coref_scores[j][i] = coref_scores[i][j]
    #         # convert numpy array to list object
    #         coref_scores = coref_scores.tolist()
    #         reformed_mentions['m_coref_scores_list'] = coref_scores
    #
    #         # save the processed cluster
    #         coref_clusters.append(reformed_mentions)
    #     return coref_clusters


