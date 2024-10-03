#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

const std::string DefaultPath = "./ʵ��2_�ַ�������/ʵ��2.2_���ĵ���������.txt";
using IndexTable = std::unordered_map<std::string, std::vector<int>>;

// ��ȡ�ļ�
std::ifstream ReadFile()
{
	std::ifstream in(DefaultPath);
	if (!in.is_open())
	{
		std::cerr << "Open failed..." << std::endl;
		exit(1);
	}

	return in;
}

// �����ʻ�������
void BuildTable(std::ifstream& file, IndexTable& table)
{
	int index = 1; // ����
	std::string line; // ��ȡÿһ��
	std::string word; // ��ȡÿһ�е�һ������
	while (getline(file, line))
	{
		std::stringstream ss(line);
		while (ss >> word)
		{
			table[word].push_back(index);
			index++;
		}
	}
}

bool SearchWord(IndexTable table, std::string& word)
{
	auto pos = table.find(word);
	if (pos != table.end())
	{
		std::cout << pos->first << ": ";
		std::for_each(pos->second.begin(), pos->second.end(), [](const int& val) {std::cout << val << " "; });
		std::cout << std::endl;
		
		return true;
	}

	return false;
}

int main()
{
	std::ifstream in = ReadFile();
	
	IndexTable table;
	BuildTable(in, table);
	
	while (true)
	{
		std::string word;
		std::cout << "Please Enter��q is quit��# ";
		std::cin >> word;

		if (word == "q") break;

		if (!SearchWord(table, word)) std::cout << word << " does not exist !!!" << std::endl;
	}

	return 0;
}