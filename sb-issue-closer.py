import json

import click
import requests


@click.command()
@click.option("--base-url",
              help="The base URL for the Storyboard API.",
              required=True)
@click.option("--project-id",
              help="The ID of the project to close tasks for. Get me by using dev tools in your browser.",
              required=True)
@click.option("--message",
              help="The message to use when closing tasks as invalid.",
              required=True)
@click.option("--token",
              help="The Storyboard API token to use for authentication.",
              required=True)
def closer(base_url: str, project_id: int, message: str, token: str) -> None:
        """Close all tasks as INVALID for a given project."""
        common_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {token}"
        }
        # Make a GET request to retrieve a list of all stories for the project
        stories_url = f"{base_url}/stories?project_id={project_id}&status=active"

        response = requests.get(stories_url, headers=common_headers)
        if response.status_code != 200:
            print("Failed to retrieve stories for {}".format(project_id))
            exit(1)

        stories = json.loads(response.text)

        # Iterate through each story and close all tasks as invalid
        for story in stories:
            try:
                tasks_url = f"{base_url}/tasks?story_id={story['id']}"
                response = requests.get(tasks_url)
                tasks = json.loads(response.text)
            except Exception as e:
                print("While processing story: {}, encountered exception: {}".format(story, e))
                continue
            for task in tasks:
                if task['status'] != "Todo":
                    if task['status'] == "In Progress":
                        print("Skipping task {} for story {} because it is in progress.".format(story['id'], task['id']))
                    continue
                try:
                    payload = {
                        "status": "Invalid",
                        "message": message
                    }
                    task_url = f"{base_url}/tasks/{task['id']}"
                    response = requests.put(task_url, json=payload)
                    if response.status_code == 200:
                        print(f"Closed task {task['id']} for story {story['id']}")
                    else:
                        print(f"Failed to close task {task['id']} for story {story['id']}")
                except Exception as e:
                    print("While processing task: {} in story {}, encountered exception: {}".format(task, story, e))
        
        print("All tasks have been closed.")


if __name__ == "__main__":
    closer()