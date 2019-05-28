import requests
import argparse
import git
import os

API_VERSION = 'v4'

def get_args():
    parser = argparse.ArgumentParser()
    gitlab_cloner = parser.add_argument_group('gitlab-cloner')
    gitlab_cloner.add_argument('--host', type=str, help='GitLab host', required=True)
    gitlab_cloner.add_argument('--token', type=str, help='Private token', required=True)
    return parser.parse_args()

def retrieve_projects(host: str, token: str):
    page = '1'
    projects = []
    while True:
        response = requests.get(
            f'https://{host}/api/{API_VERSION}/projects',
            params={'private_token': token, 'page': page},
        )
        projects.extend([{
            'id': project['id'],
            'name': project['name'],
            'group': project['namespace']['full_path'], 
            'http': project['http_url_to_repo']
        } for project in response.json()])
        page = response.headers.get('X-Next-Page')
        if not page:
            break
    return projects

def clone_repo(url: str, relative_path: str):
    return git.Repo.clone_from(url, relative_path)

def main():
    args = get_args()
    print('Retrieving projects...')
    projects = retrieve_projects(host=args.host, token=args.token)
    print(f'Retrieved {len(projects)} projects successfully!')
    for project in projects:
        print(f"Cloning project {project['name']} with id: {project['id']}")
        clone_repo(
            url=project['http'],
            relative_path=os.path.join(project['group'], project['name'])
        )
    print(f'Cloned {len(projects)} projects successfully!')
