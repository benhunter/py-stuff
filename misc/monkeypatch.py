# Trying out monkeypatch

def needs_input():
    from_input = input()
    return from_input


def test_needs_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 'monkey')
    assert input()=='monkey'
    assert needs_input()=='monkey'


if __name__ == '__main__':
    print(needs_input())

