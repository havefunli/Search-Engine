//#include <iostream>
//#include <fstream>
//#include <sstream>
//#include <vector>
//#include <string>
//#include <algorithm>
//#include <unordered_map>
//
//const std::string DefaultPath = "./ʵ��2_�ַ�������/ʵ��2_1�����ʻ�������_����.txt";
//const std::string DefalutSep = " ";
//using Locations = std::vector<std::string>;
//using IndexTable = std::unordered_map<std::string, Locations>;
//
//
//// ��ȡ�ļ�����
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
//// ��ȡÿ������
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
//// ����������
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
//		// ���һ������
//		if (pos == std::string::npos)
//		{
//			word = Content;
//			idtable[word].push_back(SerialNum);
//			break;
//		}
//		// ���������ĵ���
//		word = Content.substr(0, pos);
//		idtable[word].push_back(SerialNum);
//
//		// ȥ�����ӵĵ���
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