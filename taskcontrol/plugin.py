# Plugins Base


class PluginsBase():

    # return plugin instance/module
    def plugin_create(self, name, task_instance):

        # TODO: Apply multiple instances (Allow seperate and merged instances)
        # Low priority
        if type(task_instance) != dict:
            raise TypeError("plugins definition has an issue")

        if type(task_instance) == dict:
            # if not task_instance.get("config"):
            #     raise ValueError("config definition has an issue")
            # if not task_instance.get("ctx"):
            #     raise ValueError("ctx definition has an issue")
            # if not task_instance.get("plugins"):
            #     raise ValueError("internal plugins definition has an issue")
            # if not task_instance.get("shared"):
            #     raise ValueError("shared definition has an issue")
            # if not task_instance.get("tasks"):
            #     raise ValueError("tasks definition has an issue")
            pass

        if type(name) == str:
            return {
                name: {
                    "config": task_instance.get("config"),
                    "ctx": task_instance.get("ctx"),
                    "plugins": task_instance.get("plugins"),
                    "shared": task_instance.get("shared"),
                    "tasks": task_instance.get("tasks")
                }
            }

