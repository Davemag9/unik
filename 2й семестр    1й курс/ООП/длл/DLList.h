#ifndef UNTITLED_DLLIST_H
#define UNTITLED_DLLIST_H
#define MAX_STR_LEN 256
#include <bits/stdc++.h>

using namespace std;

class IList {
public:
    virtual void addTail() = 0;
    virtual void addHead() = 0;
    virtual void interface() = 0;
    virtual void deleteN() = 0;
    virtual void addKHead() = 0;
    virtual void clr() = 0;
    virtual void addKTail() = 0;
};


class DLList : public IList {
private:
    struct Node {
        char *key;
        Node *next = nullptr;
        Node *prev = nullptr;

        void setKey(const string &str) {
            key = new char[MAX_STR_LEN]();
            strcpy(key, str.c_str());
        }

        void print() {
            puts(key);
        }
    };

public:
    Node *head = nullptr;
    Node *tail = nullptr;
    int size = 0;

    void create();
    void print() const;
    void addTail() override;
    void addHead() override;
    void interface() override;
    void deleteN() override;
    void addKHead() override;
    void clr() override;
    virtual void addKTail() override;

};

#endif //UNTITLED_DLLIST_H