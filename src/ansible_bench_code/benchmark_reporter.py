from datetime import datetime

class Reporter:
    def __init__(
        self,
        start_time=None,
        failed_initial_molecule_test=None,
        failed_at_stage_yamllint=None,
        failed_at_stage_ansiblelint=None,
        failed_at_stage_molecule_test=None,
        passed_all_stages=None,
        report_path=None,
        yamllint_runs=0,
        yamllint_passed_without_iteration=0,
        yamllint_passed_at_first_attempt=0,
        ansiblelint_runs=0,
        ansiblelint_passed_at_first_attempt=0,
        failed_with_exception=None,
    ):
        self._start_time = start_time
        self._failed_initial_molecule_test = failed_initial_molecule_test
        self._failed_at_stage_yamllint = failed_at_stage_yamllint
        self._failed_at_stage_ansiblelint = failed_at_stage_ansiblelint
        self._failed_at_stage_molecule_test = failed_at_stage_molecule_test
        self._passed_all_stages = passed_all_stages
        self._report_path = report_path
        self._yamllint_runs = yamllint_runs
        self._yamllint_passed_without_iteration = yamllint_passed_without_iteration
        self._yamllint_passed_at_first_attempt = yamllint_passed_at_first_attempt
        self._ansiblelint_runs = ansiblelint_runs
        self._ansiblelint_passed_at_first_attempt = ansiblelint_passed_at_first_attempt
        self._failed_with_exception = failed_with_exception or []

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def failed_initial_molecule_test(self):
        return self._failed_initial_molecule_test

    @failed_initial_molecule_test.setter
    def failed_initial_molecule_test(self, value):
        self._failed_initial_molecule_test = value

    @property
    def failed_at_stage_yamllint(self):
        return self._failed_at_stage_yamllint

    @failed_at_stage_yamllint.setter
    def failed_at_stage_yamllint(self, value):
        self._failed_at_stage_yamllint = value

    @property
    def failed_at_stage_ansiblelint(self):
        return self._failed_at_stage_ansiblelint

    @failed_at_stage_ansiblelint.setter
    def failed_at_stage_ansiblelint(self, value):
        self._failed_at_stage_ansiblelint = value

    @property
    def failed_at_stage_molecule_test(self):
        return self._failed_at_stage_molecule_test

    @failed_at_stage_molecule_test.setter
    def failed_at_stage_molecule_test(self, value):
        self._failed_at_stage_molecule_test = value

    @property
    def passed_all_stages(self):
        return self._passed_all_stages

    @passed_all_stages.setter
    def passed_all_stages(self, value):
        self._passed_all_stages = value

    @property
    def report_path(self):
        return self._report_path

    @report_path.setter
    def report_path(self, value):
        self._report_path = value

    @property
    def yamllint_runs(self):
        return self._yamllint_runs

    @yamllint_runs.setter
    def yamllint_runs(self, value):
        self._yamllint_runs = value

    @property
    def yamllint_passed_without_iteration(self):
        return self._yamllint_passed_without_iteration

    @yamllint_passed_without_iteration.setter
    def yamllint_passed_without_iteration(self, value):
        self._yamllint_passed_without_iteration = value

    @property
    def yamllint_passed_at_first_attempt(self):
        return self._yamllint_passed_at_first_attempt

    @yamllint_passed_at_first_attempt.setter
    def yamllint_passed_at_first_attempt(self, value):
        self._yamllint_passed_at_first_attempt = value

    @property
    def ansiblelint_runs(self):
        return self._ansiblelint_runs

    @ansiblelint_runs.setter
    def ansiblelint_runs(self, value):
        self._ansiblelint_runs = value

    @property
    def ansiblelint_passed_at_first_attempt(self):
        return self._ansiblelint_passed_at_first_attempt

    @ansiblelint_passed_at_first_attempt.setter
    def ansiblelint_passed_at_first_attempt(self, value):
        self._ansiblelint_passed_at_first_attempt = value

    @property
    def failed_with_exception(self):
        return self._failed_with_exception

    @failed_with_exception.setter
    def failed_with_exception(self, value):
        if not isinstance(value, list):
            raise ValueError("failed_with_exception muss eine Liste sein.")
        self._failed_with_exception = value


    def reports(
        self,
    ) -> None:
        """
        Creates a report file with start/end time, duration, stage counts,
        total entries and detailed list of results.
        """
        report_file = self._report_path / "report.txt"

        end_time = datetime.now()
        duration = end_time - self._start_time
    
        with report_file.open("w", encoding="utf-8") as f:
            f.write("====== Run Summary ======\n")
            f.write(f"Start time : {self._start_time}\n")
            f.write(f"End time   : {end_time}\n")
            f.write(f"Duration   : {duration}\n\n")

            f.write("====== Stage Counts ======\n")
            if len(self._failed_initial_molecule_test) > 0:
                f.write(f"Initial molecule failures: {len(self._failed_initial_molecule_test)}\n")
            if len(self._failed_with_exception) > 0:
                f.write(f"Failed with exception   : {len(self._failed_with_exception)}\n")
            f.write(f"yamllint failures   : {len(self._failed_at_stage_yamllint)}\n")
            f.write(f"ansiblelint failures: {len(self._failed_at_stage_ansiblelint)}\n")
            f.write(f"molecule failures   : {len(self._failed_at_stage_molecule_test)}\n")
            f.write(f"all passed          : {len(self._passed_all_stages)}\n")
            total = (
                len(self._failed_at_stage_yamllint)
                + len(self._failed_at_stage_ansiblelint)
                + len(self._failed_at_stage_molecule_test)
                + len(self._passed_all_stages)
            )
            f.write(f"TOTAL entries       : {total}\n\n")

            if (total > 0):
                yamllint_passed = len(self._failed_at_stage_ansiblelint) + len(self._failed_at_stage_molecule_test) + len(self._passed_all_stages)
                ansible_lint_passed = len(self._failed_at_stage_molecule_test) + len(self._passed_all_stages)

                yamllint_score = 1 + (
                    (self._yamllint_passed_without_iteration + self._yamllint_passed_at_first_attempt)
                    / (2 * self._yamllint_runs)
                    if self._yamllint_runs > 0 else 0
                )

                ansiblelint_score = 1 + (
                    (self._ansiblelint_passed_at_first_attempt / self._ansiblelint_runs)
                    if self._ansiblelint_runs > 0 else 0
                )

                molecule_passed = len(self._passed_all_stages) 

                benchmark_score = (
                    (yamllint_score * (yamllint_passed / total))
                    + 2 * (ansiblelint_score * (ansible_lint_passed / total))
                    + 4 * (molecule_passed / total)
                ) / (1 * 2 + 2 * 2 + 4)


                f.write("====== KPIs ======\n")
                f.write(f"Yamllint passed         :  {yamllint_passed}\n")
                f.write(f"Ansible-lint passed     :  {ansible_lint_passed}\n")
                f.write(f"Molecule passed         :  {molecule_passed}\n")
                f.write(f"YAMLLint Score          :  {yamllint_score:.4f}\n")
                f.write(f"Ansible-Lint Score      :  {ansiblelint_score:.4f}\n")
                f.write(f"Benchmark-Score         :  {benchmark_score:.4f}\n\n")
            else:
                f.write("No entries were processed, so no KPIs can be calculated.\n\n")

            f.write("====== Detailed Entries ======\n")
            if len(self._failed_initial_molecule_test) > 0:
                f.write("\nInitial Molecule Test Statistics: \n")
                f.write(f"Initial molecule failures: {len(self._failed_initial_molecule_test)}\n")
                for entry in self._failed_initial_molecule_test:
                    f.write(f"Initial molecule failed: {entry}\n")
            if len(self._failed_with_exception) > 0:
                f.write("\nFailed with Exception Statistics: \n")
                f.write(f"Failed with exception   : {len(self._failed_with_exception)}\n")
                for entry in self._failed_with_exception:
                    f.write(f"Failed with exception: {entry}\n")
            f.write("\nYAMLLINT Statistics: \n")
            f.write(f"Total yamllint runs: {self._yamllint_runs}\n")
            f.write(f"Yamllint passed without iteration: {self._yamllint_passed_without_iteration}\n")
            f.write(f"Yamllint passed at first attempt: {self._yamllint_passed_at_first_attempt}\n")
            f.write("Failed at stage 'yamllint': \n")
            for entry in self._failed_at_stage_yamllint:
                f.write(f"yamllint failed: {entry}\n")
            f.write("\nANSIBLELINT Statistics: \n")
            f.write(f"Total ansiblelint runs: {self._ansiblelint_runs}\n")
            f.write(f"Ansiblelint passed at first attempt: {self._ansiblelint_passed_at_first_attempt}\n")
            f.write("Failed at stage 'ansiblelint':\n")
            for entry in self._failed_at_stage_ansiblelint:
                f.write(f"ansiblelint failed: {entry}\n")

            f.write("\nMOLECULE Statistics: \n")     
            f.write("failed at stage 'molecule-test':\n")
            for entry in self._failed_at_stage_molecule_test:
                f.write(f"molecule failed: {entry}\n")
            f.write("\nSuccessfully passed all stages:\n")
            for entry in self._passed_all_stages:
                f.write(f"passed: {entry}\n")

            f.write("\n====== All run roles ======\n")
            for entry in self._failed_at_stage_yamllint:
                f.write(f"{entry}\n")
            for entry in self._failed_at_stage_ansiblelint:
                f.write(f"{entry}\n")
            for entry in self._failed_at_stage_molecule_test:
                f.write(f"{entry}\n")
            for entry in self._passed_all_stages:
                f.write(f"{entry}\n") 
