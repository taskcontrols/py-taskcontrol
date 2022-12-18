# for git development repo
from taskcontrol import task, Workflow

# for package
# from taskcontrol import task, Workflow


# Instance of tasks and apis object
# Every instance will store it own list of tasks
#       with their before/after middlewares
sparrow = Workflow()

# Example five for decorator usage with kwarg as function
@task(name="taskfive",
          task_instance=sparrow,
          task_order=4,
          shared=False,
          args=[1, 2],
          # Declare kwargs as a dict object or a function
          kwargs={},
          after=[],
          log=False
          )
def taskfive(ctx, result, *args, **kwargs):
    print("Running my task function: taskfive")
    return args, kwargs


run_0 = sparrow.start(tasks=["taskfive", {}])
print("\nrun_0 2 Tasks [2I]", run_0)
