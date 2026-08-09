import boto3
from dotenv import load_dotenv

sessions = boto3.Session()

def get_profiles():

    profiles = sessions.available_profiles
    return profiles



def build_session(profile,region_name):

    if profile == "__env__":
        load_dotenv()
        session_root = boto3.Session(region_name=region_name)
        return  session_root

    session_root = boto3.Session(profile_name=profile,region_name=region_name)
    return session_root

    
