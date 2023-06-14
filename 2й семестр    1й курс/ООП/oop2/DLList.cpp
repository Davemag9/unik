//
// Created by davem on 09.04.2022.
//
#include <bits/stdc++.h>
#include "DLList.h"
using namespace std;
void DLList::create() {
    cout << "Size:";
    int k;
    cin >> k;
    while (k < 0) {
        cout << "Size must be >=0. Try one more time)";
        cin >> k;
    }
    for (int i = 0; i < k; ++i) {
        Node* node = new Node;
        cout << "Value:";
        string s;
        cin >> s;
        node->setKey(s);
        if (head == nullptr) {
            head = node;
            tail = head;
        }
        else {
            node->prev = tail;
            node->next = nullptr;
            tail->next = node;
            tail = node;
        }
        size++;
    }
    cout << "DLList created." << endl;
}

void DLList::print() const {
    if (size == 0 or !head) {
        cout << "Empty list" << endl;
    }
    else {
        int i = 0;
        Node* node = head;
        while (node) {
            cout << ++i << ")";
            node->print();
            node = node->next;
        }
    }
}

void DLList::addTail() {
    Node* node = new Node;
    cout << "Value:";
    string s;
    cin >> s;
    node->setKey(s);
    if (head == nullptr) {
        head = node;
        tail = head;
    }
    else {
        node->prev = tail;
        node->next = nullptr;
        tail->next = node;
        tail = node;
    }
    size++;
    cout << "Element added to tail." << endl;
}

void DLList::addHead() {
    Node* node = new Node;
    cout << "Value:";
    string s;
    cin >> s;
    node->setKey(s);
    if (head == nullptr) {
        head = node;
        tail = head;
    }
    else {
        node->prev = nullptr;
        node->next = head;
        head->prev = node;
        head = node;
    }
    size++;
    cout << "Element added to head." << endl;
}

void DLList::interface() {
    cout << "DLList menu:\n1.Add to tail\n2.Add to head\n3.Print list\n4.Clear\n5.Restart\n6.Delete N\n7.Add k to head\n8.Add k to tail\n0.End\n";
    string str;
    cin >> str;
    if (str.length() != 1 or !(str[0] >= '0' and str[0] <= '9')) {
        cout << endl << endl << "Wrong input." << endl;
        return interface();
    }
    switch (str[0]) {
        case '1':
            addTail();
            break;
        case '2':
            addHead();
            break;
        case '3':
            print();
            break;
        case '4':
            clr();
            break;
        case '5':
            clr();
            create();
            break;
        case '6':
            deleteN();
            break;
        case '7':
            addKHead();
            break;
        case'8':
            addKTail();
            break;
        case'9':
            cout << "That button doesn`t do anything((" << endl;
            break;
        case '0':
            cout << endl << endl << "Thats all." << endl;
            return;
    }
    cout << endl;
    return interface();
}

void DLList::clr() {
    Node* node = tail;
    Node* next;
    while (node) {
        next = node->prev;
        delete node;
        node = next;
    }
    head = nullptr;
    tail = nullptr;
    size = 0;
    cout << "DLList cleared." << endl;
}


void DLList::deleteN() {
    Node* toDelete = nullptr;
    Node* node = head;
    int n;
    cout << "Chose n to delete:";
    cin >> n;
    if (n > size or n <= 0) {
        cout << "Look carefully" << endl;
        return deleteN();
    }
    if (size == 0 or !head) {
        cout << "Empty list" << endl;
    }
    int i = 1;
    while (node != nullptr) {
        if (i == n) {
            toDelete = node;
            node = node->prev;
            if (node) {
                node->next = node->next->next;
                if (node->next) node->next->prev = node;
            }
            else {
                if (toDelete->next) head = toDelete->next;
                else {
                    head = nullptr;
                    tail = nullptr;
                }
                if (head) head->prev = nullptr;
                node = head;
            }
            delete toDelete;
            size--;
            break;
        }
        node = node->next;
        i++;
    }
}
void DLList::addKHead() {
    int k;
    cout << "Number of elements to add:";
    cin >> k;
    if (k < 0) {
        cout << "Nice choose,but you must retry :)" << endl;
        return addKHead();
    }
    else {
        for (int j = 0; j < k; j++) {
            addHead();
        }
    }
    cout << "Elements added." << endl;
}

void DLList::addKTail() {
    int k;
    cout << "Number of elements to add:";
    cin >> k;
    if (k < 0) {
        cout << "Nice choose,but you must retry :)" << endl;
        return addKTail();
    } else {
        for (int j = 0; j < k; j++) {
            addTail();
        }
    }
    cout << "Elements added." << endl;
}

