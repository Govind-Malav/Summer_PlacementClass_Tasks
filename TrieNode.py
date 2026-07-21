class TrieNode:
    def __init__(self):
        self.children={}
        self.is_end_of_word=False

class Autocompletesystem:
    def __init__(self):
        self.root=TrieNode()
    def insert_word(self,word):
        current=self.root
        for char in word:
            if char not in current.children:
                current.children[char]= TrieNode()
            current=current.children[char]
        current.is_end_of_word=True

    def search_prefix(self,prefix):
        current=self.root
        for char in prefix:
            if char not in current.children:
                return False
            current=current.children[char]
        return True

def collect_words(node,current_word,result):
    if node.is_end_of_word:
        result.append(current_word)
    for char,child_node in node.children.items():
        collect_words(child_node,current_word+char,result)

def get_suggestions(trie_system,prefix):
    current= trie_system.root
    for char in prefix:
        if char not in current.children:
            return []
        current=current.children[char]

    suggestions=[]
    collect_words(current,prefix,suggestions)
    return suggestions

engine=Autocompletesystem()
for word in ['apple','banana','appricot','cherry','avocado','blueberry']:
    engine.insert_word(word)

print("suggestions for ap:")
print(get_suggestions(engine,'ap')) 