import boto3
import botocore
import json
from pprint import pprint
from os import environ
from sys import exit
from MyFunctions.methods import lastone

access_key = str(environ["AWS_ACCESS_KEY_ID"])
secret_key = str(environ["AWS_SECRET_ACCESS_KEY"])
bucket_name = str(environ["AWS_BUCKET_NAME"])
s3 = boto3.resource(
    service_name="s3", region_name="ap-northeast-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key
).Bucket(bucket_name)


class json_io_s3:
    def __init__(self, name_project: str, name_file: str):
        folder_name = name_project
        self.key = folder_name + "/" + name_file + ".json"
        self.obj = s3.Object(self.key)
        try:
            self.obj.load()
        except Exception:
            self.put({})
            try:
                self.obj.load()
            except Exception:
                print("S3エラー")
                exit(1)

    def iterate(self) -> classmethod:
        return self

    def put(self, data: dict) -> None:
        _ = self.obj.put(Body=json.dumps(data, ensure_ascii=False, indent=2))

    def get(self) -> dict:
        return json.load(self.obj.get()["Body"])


class DS:
    def __init__(
        self, name_file, name_project: str
    ):
        self.io = json_io_s3(name_file="data_bot", name_project=name_project)

    def push(self):
        dict_data = self.io.get()
        temp_dict = dict()
        if dict_data.get(self.id):
            for key in dict_data.get(self.id).keys():
                exec(f"temp=self.{key}")
                exec("temp_dict.update({key:temp})")
            temp_dict = {self.id: temp_dict}
        dict_data.update(temp_dict)
        self.io.put(dict_data)

    def pull(self):
        dict_data = self.io.get()
        # print(dict_data)
        for symbol in list(dict_data.keys()):
            temp = dict_data.get(symbol)
            data_text = str()
            if isinstance(temp, list):
                data_text = "["
                for t, flag in lastone(temp):
                    if not isinstance(t, str):
                        t = str(t)
                    else:
                        t = "'" + t + "'"
                    if flag:
                        data_text += t
                    else:
                        data_text += (t + ",")
                data_text += "]"
            elif isinstance(temp, str):
                data_text = "'" + temp + "'"
            else:
                data_text = str(temp)

            exec(f"self.{symbol}={data_text}")
        return self


class DS_empty:
    id = None

    def __init__(self, id):
        self.id = id

    def change(self, name, value):
        if name:
            if value:
                exec(f"self.{str(name)}={value}")
            else:
                exec(f"self.{str(name)}=None")


class DS_mass:

    dict_DS = dict()

    def __init__(
        self, name_file, name_project: str, DS_empty
    ):
        self.io = json_io_s3(name_file=name_file, name_project=name_project)
        self.DS_empty = DS_empty

    def pull(self):
        dict_servers = self.io.get()

        for key_1 in dict_servers.keys():
            dict_server = dict_servers.get(key_1)
            if isinstance(dict_server, dict):
                temp_DS = self.DS_empty(key_1)
                for key_2 in dict_server.keys():
                    temp = f"temp_DS.change('{key_2}',dict_server.get('{key_2}'))"
                    exec(temp)
                self.dict_DS.update({key_1: temp_DS})
        return self

    def get(self, id):
        return self.dict_DS.get(str(id))

    def delete(self, id):
        temp_dict = self.io.get()
        temp_dict.pop(id)
        self.io.put(temp_dict)

    def clear(self):
        temp_dict = self.io.get()
        temp = temp_dict.get("DEFAULT")
        temp_dict = dict()
        if temp:
            temp_dict.update({"DEFAULT": temp})
        self.io.put(temp_dict)
