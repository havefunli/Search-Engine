#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>

const std::string DefaultPath = "./实验2_字符串查找/实验2.2_单文档查找用例.txt";
using IndexTable = std::unordered_map<std::string, std::vector<int>>;

// 读取文件
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

// 建立词汇索引表
void BuildTable(std::ifstream& file, IndexTable& table)
{
	int index = 1; // 计数
	std::string line; // 读取每一行
	std::string word; // 读取每一行的一个单词
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
		std::cout << "Please Enter（q is quit）# ";
		std::cin >> word;

		if (word == "q") break;

		if (!SearchWord(table, word)) std::cout << word << " does not exist !!!" << std::endl;
	}

	return 0;
}