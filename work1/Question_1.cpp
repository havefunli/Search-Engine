//#include <iostream>
//#include <fstream>
//#include <sstream>
//#include <vector>
//#include <string>
//#include <algorithm>
//#include <unordered_map>
//
//const std::string DefaultPath = "./实验2_字符串查找/实验2_1建立词汇索引表_用例.txt";
//const std::string DefalutSep = " ";
//using Locations = std::vector<std::string>;
//using IndexTable = std::unordered_map<std::string, Locations>;
//
//
//// 读取文件内容
//std::ifstream ReadFile()
//{
//	std::ifstream in(DefaultPath);
//
//	if (!in.is_open())
//	{
//		std::cerr << "Failed open..." << std::endl;
//		exit(1);
//	}
//
//	return in;
//}
//
//// 获取每行内容
//void GetLine(std::ifstream& FileContent, std::vector<std::string>& lines)
//{
//	std::string line;
//	while (std::getline(FileContent, line))
//	{
//		std::cout << "line:" << line << std::endl;
//		lines.push_back(std::move(line));
//	}
//}
//
//// 建立索引表
//void BuildIndex(std::string& line, IndexTable& idtable)
//{
//	auto pos = line.find(DefalutSep);
//	if (pos == std::string::npos) return;
//
//	std::string SerialNum = line.substr(0, pos);
//	std::string Content = line.substr(pos + 1);
//	
//	std::string word;
//	while (true)
//	{
//		auto pos = Content.find(DefalutSep);
//		// 最后一个单词
//		if (pos == std::string::npos)
//		{
//			word = Content;
//			idtable[word].push_back(SerialNum);
//			break;
//		}
//		// 不是在最后的单词
//		word = Content.substr(0, pos);
//		idtable[word].push_back(SerialNum);
//
//		// 去除增加的单词
//		Content.erase(0, word.size() + DefalutSep.size());
//	}
//}
//
//int main()
//{
//	std::ifstream FileContent = ReadFile();
//	std::cout << "Successful open..." << std::endl;
//	
//	std::vector<std::string> lines;
//	GetLine(FileContent, lines);
//	std::cout << "Successful get all lines..."<< std::endl;
//
//	IndexTable idextable;
//	for (auto& line : lines)
//	{
//		BuildIndex(line, idextable);
//	}
//
//	for (auto& pair : idextable)
//	{
//		auto func = [](std::string& val) {std::cout << val << " "; };
//		std::cout << pair.first << ": ";
//		std::for_each(pair.second.begin(), pair.second.end(), func);
//		std::cout << std::endl;
//	}
//
//	return 0;
//}