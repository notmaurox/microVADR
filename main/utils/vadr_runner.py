import os
import subprocess
import logging

VADR_FILE_STORE = "/tmp/vadr_runs"
MODEL_DIR = os.getenv("VADRMODELDIR")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('microVadr')

class VadrRunner:

    def __init__(self, seq_name, seq, run_id):
        self.seq_name, self.seq = seq_name, seq
        self.run_id = run_id
        self.run_folder = os.path.join(
            VADR_FILE_STORE,
            str(run_id)
        )
        self.fasta_path = os.path.join(
            self.run_folder,
            f"{str(self.run_id)}_seq.fasta"
        )
        self.results_dir = os.path.join(
            self.run_folder,
            "results"
        )

    def go(self):
        logger.info('in go')
        if not os.path.isdir(self.run_folder):
            os.makedirs(self.run_folder)
            self._start_run()
        elif self._run_finished():
            self._load_results()

    def _start_run(self):
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
        logger.info(f'Starting VADR for run: {self.run_id}')
        logger.info(' '.join(vadr_cmd))
        subprocess.Popen(vadr_cmd)

    def _load_results(self):
    # parse results to dict, return dict.
        pass

    def _run_finished(self):
        # if there are results files, there are
        return False

    @staticmethod
    def is_run_dir(run_id):
        if os.path.isdir(os.path.join(VADR_FILE_STORE, str(run_id))):
            return True
        else:
            return False


    
