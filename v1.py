from dataclasses import dataclass
from os import link
from notion.block import BulletedListBlock, TextBlock, PageBlock
from notion.client import NotionClient
from pprint import pprint

from notion_client.typing import T

client = NotionClient(token_v2="a2a9a01452b469a2572c1f4918e5b938bb35f8c176300b54110c2a1f3862d80cf196dc09d7c27a12de56fc4bc9659cd311841d96e278caf2c0c54c2b74f06b9f6822bff15d4957177d8fe8564c5c")


page = client.get_block("https://www.notion.so/Aviv-Wiki-7713dadab79049a39fadadfd821008e9")

todo_page = client.get_block("https://www.notion.so/TODO-list-09eea3c614b24c58bbca8da67c23e2e5")

'''
@dataclass
class TodoItem():
    page_block : PageBlock
    page_link : str
    block_link : str
    block_id : str
    
    def get_block(self, page_block=None,page_link=None):
        page_block = self.page_block
        page_link= self.page_link
        try:
            for i in page_block.children:
                if(self.block_id in i.__repr__()):
                    return i
        except Exception as e:
            print(f"Failed to retrive block using stored page object due to the following exception:\n{e}\nAttempting again using stored link.")
'''
def has_title(block):
    try:
        if(block.title):
            return True
        elif(not block.title):
            return True
    except AttributeError:
        return False

def eraser_head(page = todo_page):
    for child in page.children:
        repr = child.__repr__()
        print(f"\nBeginning the permenant deletion process of {repr}")
        try:
            child.remove(permanently=True)
            print(f"Permenant deletion proccess of {repr} has been completed with no erros or run-time exceptions.")
        except Exception as e:
            print(f"Permenant deletion proccess of {repr} has been aborted before completion due to the following run-time exception:\n{e}\n")

    if(not page.children):
        print("Processes of all permenant child deletion have completed with SUCCESS.")
    else:
        print("Processes of all permenant child deletion have completed with FAILURE.")

def write_head(links,page = todo_page):
    '''
    The write_head function writes to a designated page
    '''
    for i in links:
        page.children.add_new(BulletedListBlock, title = f"[{i[1]}]({i[0]})")

def file_comb(page=page,target = "TODO",links = []):
    '''
    The file_comb function combs though the specified file for the target phrase
    '''
    page_children = page.children
    c_links = links
    if(not page_children):
        if(has_title(page) and target in page.title):
                c_links.append((page.get_browseable_url(),page.title))
        return c_links
    for i in page_children:
        if "view" in i.__repr__().split(" ")[0].lower():
            if(i.views):
                for j in i.views[0].default_query().execute():
                    file_comb(j,"TODO",c_links)
            elif(not i.views):
                return c_links
        elif("block" in i.__repr__().split(" ")[0].lower()):
            file_comb(i,"TODO",c_links)
            if(has_title(i) and target in i.title and (i.get_browseable_url(),i.title) not in c_links):
                c_links.append((i.get_browseable_url(),i.title))
    return c_links



if __name__ == "__main__":
    print("started combing")
    links = file_comb()
    print("combing complete")
    print("started erasing")
    eraser_head()
    print("erasing complete")
    print("starting writing")
    write_head(links)
    print("completed writing")
