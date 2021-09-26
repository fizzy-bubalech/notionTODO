from notion.block import BulletedListBlock, TextBlock
from notion.client import NotionClient
from pprint import pprint

client = NotionClient(token_v2="a2a9a01452b469a2572c1f4918e5b938bb35f8c176300b54110c2a1f3862d80cf196dc09d7c27a12de56fc4bc9659cd311841d96e278caf2c0c54c2b74f06b9f6822bff15d4957177d8fe8564c5c")


page = client.get_block("https://www.notion.so/Test-page-3ec47b5d6202464ab9b831a099b4aa35")

todo_test_page = client.get_block("https://www.notion.so/TODO-TEST-PAGE-09eea3c614b24c58bbca8da67c23e2e5")

#pprint(page.children[0])


def test():
    """
    This test was to see if and how to change the text of elements in the page
    """
    page.children[0].title = "Test success: TRUE"
    if(page.children[0].title == "Test success: TRUE"):
        print(page.children[0].title)
    else:
        print("FAILURE")


def test1():
    return page.children[1].views[0].default_query().execute()[0]

def test2(block = page, links = []):
    """
    This test was to see if I could extract the links for all the places in the page and its children where it said 'FALSE'
    """
    page_children = block.children
    c_links = links
    print(f"Line 26:{page_children}")
    #print(f"Line 27:{(not page_children)}")
    if(not page_children):
        #print(f"Line 29:{block.title}")
        if("FALSE" in block.title):
                c_links.append((block.get_browseable_url(),block.id))
                pprint("what??")
        return c_links
    for i in page_children:
        print(f"Line 35:{i.__repr__().lower()}")
        if "view" in i.__repr__().lower():
            pprint("line 31")
            if(i.views):
                for j in i.views[0].default_query().execute():
                    test2(j,c_links)
            elif(not i.views):
                return c_links
        elif("block" in i.__repr__().lower()):
            test2(i,c_links)
            if("FALSE" in i.title and (i.get_browseable_url(),i.id) not in c_links):
                c_links.append((i.get_browseable_url(),i.id))
                pprint("what??")
    return c_links



def test3(block, parent = None):
    """
    This test is to see if I can extract the parent page of an element 
    """
    c_parent = parent
    print(block.parent.__repr__())
    if(not block.parent or "page" in block.parent.__repr__().lower()):
        return c_parent
    c_parent = block.parent
    test3(block.parent,c_parent)
    return c_parent


def test4(page = todo_test_page):
    """
    This test is to see how to write to a page 
    """
    page.children.add_new(BulletedListBlock, title = "Success Bullet")
    print(page.children[-1].title)

def test5(page = todo_test_page):
    """
    This test is to see if I can delete the contents of a page. 
    """
    print()
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

def test6():
    """
    To see if you can transfer block objects between functions
    """
    block = test1()
    print("test 6")
    print(block.__repr__())


def test7():
    """
    Testing types of blocks
    """
    print(page.children[0].__repr__())
    print(page.children[0].__repr__().split(" ")[0])
#pprint(test2(client.get_block("https://www.notion.so/Test-page-3ec47b5d6202464ab9b831a099b4aa35")))
#pprint(page.children[1].views[0].default_query().execute())
#test3()

test7()

