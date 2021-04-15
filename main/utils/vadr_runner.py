import os
import subprocess
import logging
import re

VADR_FILE_STORE = "/tmp/vadr_runs"
MODEL_DIR = os.getenv("VADRMODELDIR")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('microVadr')

class VadrRunner:

    def __init__(self, seq_name, seq, process_id):
        self.seq_name, self.seq = seq_name, seq
        self.process_id = process_id
        self.run_folder = os.path.join(
            VADR_FILE_STORE,
            str(process_id)
        )
        self.fasta_path = os.path.join(
            self.run_folder,
            f"{str(self.process_id)}_seq.fasta"
        )
        self.results_dir = os.path.join(
            self.run_folder,
            "results"
        )
        self.results_dict = None

    def go(self):
        logger.info(f'go called for process: {self.process_id}')
        if not os.path.isdir(self.run_folder):
            logger.info(f'making dir for process: {self.process_id}')
            os.makedirs(self.run_folder)
            self._start_run()
        elif self._run_finished():
            logger.info(f'VADR finished for process: {self.process_id}')
            self._load_results()
        else:
            logger.info(f'VADR not finished for process: {self.process_id}')

    def get_results(self):
        return self.results_dict

    def _start_run(self):
        logger.info(f'starting VADR for process: {self.process_id}')
        self._write_fasta()
        self._start_vadr()

    def _write_fasta(self):
        logger.info(f'Writing FASTA: {self.fasta_path}')
        with open(self.fasta_path, 'w') as seq_fasta:
            seq_fasta.write(f">{self.seq_name}\n{self.seq}")

    def _start_vadr(self):
        # usage comes from...
        # /opt/vadr/vadr-models/vadr-models-corona-1.2-2/00README.txt
        vadr_cmd = [
            "v-annotate.pl", "--split", "--cpu", "8", "--glsearch", "-s",
            "-r", "--nomisc", "--mkey", "corona", "--lowsim5term", "2",
            "--lowsim3term", "2",
            "--alt_fail", "lowscore,fsthicnf,fstlocnf,insertnn,deletinn",
            "--mdir", "/opt/vadr/vadr-models/vadr-models-corona-1.2-2",
            self.fasta_path, self.results_dir
        ]
        logger.info(f'Starting VADR for run: {self.process_id}')
        logger.info(' '.join(vadr_cmd))
        subprocess.Popen(vadr_cmd)

    def _load_results(self):
        ftr_results_file = os.path.join(self.results_dir, "results.vadr.ftr")
        self.results_dict = VadrResultsFtr(ftr_results_file).serialize()

    def _run_finished(self):
        # check that files to be parsed exist...
        files_to_check_for = [
            "results.vadr.fail.tbl",
            "results.vadr.pass.tbl",
            "results.vadr.cmd",
            "results.vadr.ftr"
        ]
        # if there are results files, there are
        for file_name in files_to_check_for:
            if not os.path.isfile(os.path.join(self.results_dir, file_name)):
                logger.info(f"run {self.process_id} missing {file_name} in {self.results_dir}")
                return False
        return True

    @staticmethod
    def is_run_dir(process_id):
        if os.path.isdir(os.path.join(VADR_FILE_STORE, str(process_id))):
            return True
        else:
            return False


class VadrResultsFtr:

    def __init__(self, path_to_ftr_file):
        self.file = path_to_ftr_file
        self.seq_length = None
        self.seq_vadr_status = None
        self.model = None
        self.features = []

        self._load_data_from_file()

    def _load_data_from_file(self):
        with open(self.file, "r") as res_file:
            for row in res_file:
                if row.startswith('#'):
                    continue
                else:
                    elems = re.sub(' +', 'SPLIT_STR', row).strip().split('SPLIT_STR')
                    if not self.seq_length:
                        self.seq_length = elems[2]
                        self.seq_vadr_status = elems[3]
                        self.model = elems[4]
                    feature = {
                        "type": elems[5],
                        "name": elems[6],
                        "start": elems[11],
                        "end": elems[12],
                        "seq_coords": elems[23],
                        "alerts": elems[25]
                    }
                    self.features.append(feature)

    def serialize(self):
        to_return = {
            "VADR_status": str(self.seq_vadr_status),
            "seq_length": str(self.seq_length),
            "model_used": str(self.model),
            "sequence_features": self.features
        }
        return to_return


    
