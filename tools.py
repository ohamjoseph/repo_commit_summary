import os
from langchain_community.tools import tool
from datetime import date
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv

from llm import llm

load_dotenv()

TOKEN = os.getenv("TOKEN")

class RepoCommitParams(BaseModel):
    repo_owner: str = Field(..., description="Propriétaire du dépôt (nom d'utilisateur ou organisation)")
    repo_name: str = Field(..., description="Nom du dépôt GitHub")
    start_date: date = Field(..., description="Date de début au format YYYY-MM-DD")
    end_date: date = Field(..., description="Date de fin au format YYYY-MM-DD")

class ListCommit(BaseModel):
    commits: str = Field(..., description="Les lignes des differentes commits")


def get_commits(repo_owner, repo_name, start_date, end_date):
    """
    Récupère les commits d'un dépôt GitHub sur une période donnée.

    :param repo_owner: Propriétaire du dépôt (nom d'utilisateur ou organisation).
    :param repo_name: Nom du dépôt.
    :param start_date: Date de début (format YYYY-MM-DD).
    :param end_date: Date de fin (format YYYY-MM-DD).
    :param token: Jeton d'accès GitHub.
    :return: Liste des commits.
    """

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"since": f"{start_date}T00:00:00Z", "until": f"{end_date}T23:59:59Z"}

    commits = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Erreur lors de l'accès à l'API : {response.status_code} {response.text}")

        data = response.json()
        commits.extend(data)
        # Pagination
        url = response.links.get("next", {}).get("url")

    return commits


def generate_commit_summary(commits: str):
    """
    Analyzes commits messages and produces a structured summary.

    :param commits: List or text containing commits messages.
    :return: An overall summary of the work carried out.
    """
    prompt = \
        f"""
        You are an intelligent assistant specializing in the analysis of commits data from code repositories. Your objective is to produce a clear, structured and relevant summary based on commits messages. Here are the commits messages:

        {commits}
        
        Make a summary
        
        """

    summary = llm.invoke(prompt)
    return summary.content


@tool(args_schema=RepoCommitParams)
def get_commit_in_repo(repo_owner:str, repo_name:str, start_date:date, end_date:str):
    """
        Returns the list of commits for a given period
    """
    try:
        commits = get_commits(repo_owner, repo_name, start_date, end_date)
        text = ""
        for commit in commits:
            # text += f"- {commit['commit']['author']['name']} : {commit['commit']['message']} ({commit['sha']})\n"
            text += f"- {commit['commit']['message']}\n"

        return generate_commit_summary(text)

    except Exception as e:
        print(f"Erreur : {e}")






