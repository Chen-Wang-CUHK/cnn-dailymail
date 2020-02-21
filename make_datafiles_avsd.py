import os
import argparse

from utils import write_to_tar, init_logger


if __name__ == '__main__':
    dataset = "AVSD"
    parser = argparse.ArgumentParser(description="make_datafiles_{}.py".format(dataset))
    parser.add_argument("--data_path", "-data_path", type=str,
                        default="/apdcephfs/share_916081/rickywchen/code/DialogueSum/dataset/{}/1_preprocessed_from_raw".format(dataset))
    parser.add_argument("--save_path", "-save_path", type=str,
                        default="/apdcephfs/share_916081/rickywchen/code/DialogueSum/dataset/{}/3_cnn_daily_style_processed".format(dataset))
    parser.add_argument("--min_src_len", "-min_src_len", type=int, default=15)
    parser.add_argument("--min_sum_len", "-min_sum_len", type=int, default=1)
    parser.add_argument("--log_file", "-log_file", type=str,
                        default="logs/{}_cnn_daily_style_process_log.txt".format(dataset))
    opts = parser.parse_args()

    # Create some new directories
    if not os.path.exists(opts.save_path):
        os.makedirs(opts.save_path)
    if not os.path.exists(os.path.dirname(opts.log_file)):
        os.makedirs(os.path.dirname(opts.log_file))

    init_logger(opts.log_file)

    # Read the tokenized stories, do a little postprocessing
    # then write to bin files
    write_to_tar(
        dial_file=os.path.join(opts.data_path, 'AVSD_dialogue_minSumLen5_srcTrunc400_tgtTrunc100_spacy_test.txt'),
        sum_file=os.path.join(opts.data_path, 'AVSD_summary_minSumLen5_srcTrunc400_tgtTrunc100_spacy_test.txt'),
        out_file=os.path.join(opts.save_path, "test.tar"))
    write_to_tar(
        dial_file=os.path.join(opts.data_path, 'AVSD_dialogue_minSumLen5_srcTrunc400_tgtTrunc100_spacy_valid.txt'),
        sum_file=os.path.join(opts.data_path, 'AVSD_summary_minSumLen5_srcTrunc400_tgtTrunc100_spacy_valid.txt'),
        out_file=os.path.join(opts.save_path, "val.tar"))
    write_to_tar(
        dial_file=os.path.join(opts.data_path, 'AVSD_dialogue_minSumLen5_srcTrunc400_tgtTrunc100_spacy_train.txt'),
        sum_file=os.path.join(opts.data_path, 'AVSD_summary_minSumLen5_srcTrunc400_tgtTrunc100_spacy_train.txt'),
        out_file=os.path.join(opts.save_path, "train.tar"),
        makevocab=True,
        min_src_len=opts.min_src_len,
        min_sum_len=opts.min_sum_len)