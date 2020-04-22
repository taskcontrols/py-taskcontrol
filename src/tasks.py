# # Project Workflow


from sys import path
path.append('./')

from .bases import WorkflowBase

class Tasks(WorkflowBase):

    def add_plugin(self, plugin_inst):
        pass

    def merge(self, inst, shared=False, clash_prefix=None):
        if shared == True:
            self.shared_tasks.tasks = self.merge_tasks(
                self.shared_tasks.tasks, inst, shared, clash_prefix
            )
        elif shared == False:
            self.tasks = self.merge_tasks(
                self.tasks, inst, shared, clash_prefix
            )

    def run(self, tasks):
        print("Workflow task list provided being instantiated: ", str(tasks))
        print("Workflow has tasks: ", str(self.tasks.keys()))
        print(
            "Workflow has shared tasks: ", str(
                self.shared_tasks.tasks.keys()
            )
        )
        result = []

        if isinstance(tasks, str):
            # Iterate task through single task
            result.append(self.run_task(tasks))
        elif isinstance(tasks, list):
            # Iterate task through tasks
            [result.append(self.run_task(task_)) for task_ in tasks]
        else:
            print("No workflow or task available to run")
        return result

__all__ = ["Tasks"]
