from collections import defaultdict
from typing import OrderedDict
from notion.client import NotionClient
from notion.block import PageBlock, BulletedListBlock, SubheaderBlock
from pprint import pprint

class TodoList:
    client : NotionClient
    target_page : PageBlock
    todo_page : PageBlock
    todo_instances : defaultdict = defaultdict(lambda: None)

    def __init__(self, v2_token:str, target_page_url_or_id:str, todo_page_url_or_id:str) -> None:
        self.client = NotionClient(token_v2=v2_token)
        self.target_page = self.client.get_block(target_page_url_or_id)
        self.todo_page = self.client.get_block(todo_page_url_or_id)
    
    def erase_page_content(self, target_page:PageBlock) -> None:
        for child in target_page.children:
            child.remove(permanently=True)
        if(not target_page.children):
            print("deletion completed")
        else:
            print("deletion failed")

    def write_to_page(self, todo_instances_dict:defaultdict, target_page:PageBlock):
        '''
        The write_head function writes to a designated page
        '''
        if(not todo_instances_dict):
            #pprint(todo_instances_dict.items())
            return
        ordered_todo_dict = self.sort_dict(todo_instances_dict)
        pprint(ordered_todo_dict.items())
        current_page = list(ordered_todo_dict.keys())[0]
        for page_title, block_text in ordered_todo_dict.items():
            if(page_title is not current_page):
                target_page.children.add_new(SubheaderBlock, title = page_title)
            target_page.children.add_new(BulletedListBlock,title = block_text)

    def file_comb(self, page:PageBlock, target_phrase:str, links:defaultdict) -> defaultdict:
        """
        The file_comb function combs though the specified file for the target phrase
        """
        page_children = page.children
        
        c_links = self.todo_instances
        if(not page_children):
            if(hasattr(page,'title') and target_phrase in page.title):
                c_links[page.get_browseable_url()] = (page.title,self.get_block_parent_page(page).title) if self.get_block_parent_page(page) else (page.title,"Aviv Wiki")
            return c_links
        for child_block in page_children:
            if "view" in child_block.__repr__().split(" ")[0].lower():
                if(child_block.views):
                    for j in child_block.views[0].default_query().execute(): ##PROBLEM HERE
                        self.file_comb(j,"TODO",c_links)
                elif(not child_block.views):
                    return c_links
            elif("block" in child_block.__repr__().split(" ")[0].lower()):
                self.file_comb(child_block,"TODO",c_links)
                if(hasattr(child_block,'title') and target_phrase in child_block.title and c_links[child_block.get_browseable_url()] is None):
                    c_links[child_block.get_browseable_url()] = (child_block.title,self.get_block_parent_page(child_block).title) if self.get_block_parent_page(child_block) else (child_block.title,"Aviv Wiki")
        return c_links   
    
    def get_block_parent_page(self,block, parent = None):
        """
        Extracts the parent page of a block 
        """
        c_parent = parent
        if(not block.parent or "page" in block.parent.__repr__().split(" ")[0].lower()):
            return c_parent
        c_parent = block.parent
        self.get_block_parent_page(block.parent,c_parent)
        return c_parent

    def sort_dict(self,links:defaultdict):
        links_dict = OrderedDict()
        for block_link, title_page_tuple in links.items():
            value_block_title_link = f"[{title_page_tuple[0]}]({block_link})"
            key_page = title_page_tuple[1]
            links_dict[key_page] = value_block_title_link
        #pprint(links_dict.items())
        return OrderedDict(sorted(links_dict.items()))
    
class TodoListGenerator(TodoList):
    
    def __init__(self, v2_token: str, target_page_url_or_id: str, todo_page_url_or_id: str) -> None:
        super().__init__(v2_token, target_page_url_or_id, todo_page_url_or_id)
    
    def genrate_list(self) -> None:
        links = self.file_comb(self.target_page,"TODO",self.todo_instances)
        #pprint(links.items())
        self.erase_page_content(self.todo_page)
        self.write_to_page(links,self.todo_page)

if(__name__ == "__main__"):
    genrator = TodoListGenerator(
        "a2a9a01452b469a2572c1f4918e5b938bb35f8c176300b54110c2a1f3862d80cf196dc09d7c27a12de56fc4bc9659cd311841d96e278caf2c0c54c2b74f06b9f6822bff15d4957177d8fe8564c5c",
        "https://www.notion.so/Aviv-Wiki-7713dadab79049a39fadadfd821008e9",
        "https://www.notion.so/TODO-list-09eea3c614b24c58bbca8da67c23e2e5"
    )
    genrator.genrate_list()