/*这是字符串转数字，数字转字符串类似*/

#include<iostream>
#include<string>
#include<sstream>
using namespace std;
int main()
{
	string s_string="-110.4";
	double s_num;
	stringstream ss;
	ss<<s_string;		 
	/* 注意这里不能颠倒写*/
	ss>>s_num;
	cout<<s_num;

}
