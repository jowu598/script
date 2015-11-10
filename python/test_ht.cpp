#include <stdio.h>
#include <vector>
#include <string>
class TableData
{
public:
	TableData(int type, std::string name):type(type), name(name) {}
	int type;

	std::string name;	
};

class TableHeader
{
	friend class HashTable;
	int id;
	std::vector<TableData> m_chains;
};



class HashTable
{
	#define HASH(id, type) ((id) << 16 | (type))
public:
	void put(int id, int type, std::string str);
	void remove(int id, int type);
	std::string find(int id, int type);
	void show();
private:
	std::vector<TableHeader> m_table;
};

void HashTable::put(int id, int type, std::string str)
{
	for (int i = 0; i < m_table.size(); ++i) {
		if (id == m_table[i].id) {
			m_table[id].m_chains.push_back(TableData(type, str));
			return;
		}
	}

	TableHeader head;
	head.id = id;
	head.m_chains.push_back(TableData(type, str));
}

void HashTable::remove(int id, int type)
{
	std::vector<TableHeader>::iterator iter = m_table.begin();
	for (; iter != m_table.end(); ++iter) {
		if (id == iter->id) {
			m_table.erase(iter);
		}
	}
}

std::string HashTable::find(int id, int type)
{
	for (int i = 0; i < m_table.size(); ++i) {
		if (id == m_table[i].id) {
			for (int j = 0; j < m_table[i].m_chains.size(); ++j) {
				if (type == m_table[i].m_chains[j].type) {
					return m_table[i].m_chains[j].name;
				}
			}
		}
	}
}

void HashTable::show()
{
	for (int i = 0; i < m_table.size(); ++i) {
		for (int j = 0; j < m_table[i].m_chains.size(); ++j) {
			printf("id %d type %d name %s", m_table[i].id, m_table[i].m_chains[j].type, m_table[i].m_chains[j].name.c_str());
		}
	}
}




int main()
{
	HashTable tb;
	tb.put(1, 4, "aaa");
	tb.put(2, 42, "bbb");
	tb.put(2, 12, "ccc");
	tb.put(3, 22, "ddd");
	tb.put(4, 32, "eee");
	tb.put(2, 42, "bbb");


	tb.show();
	return 1;
}

