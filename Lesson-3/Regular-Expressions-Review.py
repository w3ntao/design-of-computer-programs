def search(pattern, text):
    """Return true if pattern appears anywhere in text
	   Please fill in the match(          , text) below.
	   For example, match(your_code_here, text)"""
    if pattern.startswith('^'):
        return match(pattern, text) # fill this line
    else:
        return match(pattern[1:], text) # fill this line

def test():
	assert search("baa*!", "Sheep said baaaa!")
	assert search("baa*!", "Sheep said baaaa humbug") == False
	assert match("baa*!", "Sheep said baaaa!")  == False
	assert match("baa*!", "baaaaaaaa! said the Sheep")

test()