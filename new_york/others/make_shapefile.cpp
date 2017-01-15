OGRLayer* poNewLayer;
long rowC=0;

map<int, int> statIdCntMap;
map<int, double> statX;
map<int, double> statY;

void HandPerRowP(long rId,std::vector<string> rowVals)
{

    if(rowVals.size()<2)return;
    std::string startTimeStr=UtilOper_hpp::replace_all_distinct(rowVals[1],"\"","");

    /*if( 0 == startTimeStr.find("9/1/2016")
        0 == startTimeStr.find("9/1/2016 16")||
        0 == startTimeStr.find("9/1/2016 17")||
        0 == startTimeStr.find("9/1/2016 18")||
        0 == startTimeStr.find("9/1/2016 19")||
        0 == startTimeStr.find("9/1/2016 20")||
        0 == startTimeStr.find("9/1/2016 21")||
        0 == startTimeStr.find("9/1/2016 22")||
        0 == startTimeStr.find("9/1/2016 23")
        )
    {

    }
    else
    {
        return;
    }*/

    printf("\t\r %s",startTimeStr.c_str());
    if(rowVals.size()<11) return;
    double slati = atof(UtilOper_hpp::replace_all_distinct(rowVals[5],"\"","").c_str());
    double slong = atof(UtilOper_hpp::replace_all_distinct(rowVals[6],"\"","").c_str());

    //9:ex 10:ey
    double elati = atof(UtilOper_hpp::replace_all_distinct(rowVals[9],"\"","").c_str());
    double elong = atof(UtilOper_hpp::replace_all_distinct(rowVals[10],"\"","").c_str());


    //startTimeStr
    
    int startId=atoi(UtilOper_hpp::replace_all_distinct(rowVals[3],"\"","").c_str());
    int stopId=atoi(UtilOper_hpp::replace_all_distinct(rowVals[7],"\"","").c_str());

    map<int, int>::iterator statIdIt = statIdCntMap.find(startId);
    if(statIdIt == statIdCntMap.end())
    {
        statIdCntMap.insert(make_pair(startId,1));
        statX.insert(make_pair(startId,slong));
        statY.insert(make_pair(startId,slati));
    }
    else
    {
        statIdIt->second = statIdIt->second+1;
    }

    statIdIt=statIdCntMap.find(stopId);
    if(statIdIt == statIdCntMap.end())
    {
        statIdCntMap.insert(make_pair(stopId,1));
        statX.insert(make_pair(stopId,elong));
        statY.insert(make_pair(stopId,elati));
    }
    else
    {
        statIdIt->second = statIdIt->second + 1;
    }

}


int _tmain(int argc, _TCHAR* argv[])
{
    //prinCompRegress();
    GDALAllRegister();
    OGRRegisterAll();
#ifndef _FileNameUTF8_
    CPLSetConfigOption("GDAL_FILENAME_IS_UTF8","NO");   //设置支持中文路径
#endif
    //PerRowHandle perHd;//=HandPerRowPtr;

     GDALDriver *poShpDriver;
     poShpDriver = GetGDALDriverManager()->GetDriverByName("ESRI Shapefile");
     GDALDataset *poNewShpDS;
     poNewShpDS = poShpDriver->Create("D:/R/大数据与机器学习/图形/stationPoin201501.shp", 0, 0, 0, GDT_Unknown, NULL );
     OGRwkbGeometryType geoTy=OGRwkbGeometryType::wkbPoint;
     poNewLayer = poNewShpDS->CreateLayer( "stationPoin201501", NULL, geoTy, NULL );


     {

         OGRFieldDefn statIdField( "StationId", OGRFieldType::OFTInteger );
         if( poNewLayer->CreateField( &statIdField ) != OGRERR_NONE )
         {
             printf( "Field %s failed.\n", statIdField.GetNameRef());
         }
         OGRFieldDefn useCountField( "UsedCount", OGRFieldType::OFTInteger );
         if( poNewLayer->CreateField( &useCountField ) != OGRERR_NONE )
         {
             printf( "Field %s failed.\n", useCountField.GetNameRef());
         }

     }

     try
     {
         CppCSV cpCs("D:/R/大数据与机器学习/自行车数据/201501-citibike-tripdata.csv",HandPerRowP);
     }catch(std::exception e){}
     printf("\r\n",rowC++);

     map<int,int>::iterator statIter;
     for(statIter=statIdCntMap.begin();statIter!=statIdCntMap.end();++statIter)
     {
         int statId = statIter->first;
         int countStat = statIter->second;
         map<int, double>::iterator xIter = statX.find(statId);
         map<int, double>::iterator yIter = statY.find(statId);

         OGRFeature *poNewFeature = OGRFeature::CreateFeature(poNewLayer->GetLayerDefn());
         OGRPoint *statPt = new OGRPoint(xIter->second,yIter->second);

         poNewFeature->SetField("StationId",statId);
         poNewFeature->SetField("UsedCount",countStat);

         OGRErr resErr = poNewFeature->SetGeometry(statPt);
         if(poNewLayer->CreateFeature(poNewFeature) != OGRERR_NONE )
         {
            printf( "Failed to create feature in shapefile.\n" );
         }
         printf("\t\r %ld",rowC++);
         OGRFeature::DestroyFeature( poNewFeature );
         free(statPt);
     }


    GDALClose( poNewShpDS );

    printf("main");
    getchar();
    return 0;
}


CppCSV.h

#ifndef _CPPCSV_H_
#define _CPPCSV_H_
//#include "stringparser.h"
#include <assert.h>
#include <map>
#include <vector>
#include <string>
using namespace std;

typedef unsigned long u32;
typedef void (*PerRowHandle)(long Oid,vector<string> perRowStr);

class CppCSV
{
private:
    string m_CSVName;
protected:
    map<u32, map<u32, string>> m_stringMap;


public:
    CppCSV()
    {
        m_rowHand = NULL;
    }
    CppCSV(const char *path)
    {
        m_rowHand = NULL;
        assert(LoadCSV(path));
    }
    CppCSV(const char *path,PerRowHandle rowHdl)
    {
        m_rowHand = rowHdl;
        assert(LoadCSV(path));
    }
    ~CppCSV(){}

    PerRowHandle m_rowHand;

    bool LoadCSV(const char *path);
    bool LoadCSV(const char *path,PerRowHandle perRowH);
    bool SaveCSV(const char *path = NULL);

    bool GetIntValue(u32 uiRow, u32 uiCol, int &riValue);
    bool GetFloatValue(u32 uiRow, u32 uiCol, float &rfValue);
    string* GetStringValue(u32 uiRow, u32 uiCol);

    int GetParamFromString(string str, vector<string> &stringVec, char delim  = ',');


    map<u32, map<u32, string>>& GetCSVMap()
    {
        return m_stringMap;
    }

};

#endif


CppCSV.cpp

#include "stdafx.h"
#include "CppCSV.h"
#include <stdio.h>
#include "BikeLineRow.h"
//#include "stringparser.h"

bool CppCSV::LoadCSV(const char *path)
{
    FILE *pFile = fopen(path, "r");

    if (pFile)
    {
        fseek(pFile, 0, SEEK_END);
        u32 uSize = ftell(pFile);
        rewind(pFile);

        char *fileBuffer = new char[uSize];
        fread(fileBuffer, 1, uSize, pFile);

        map<u32, string> stringMap;
        u32 uiIndex = 1;
        char *pBegin = fileBuffer;
        char *pEnd = strchr(pBegin, '\n');


        pBegin = pEnd + 1;
        pEnd = strchr(pBegin, '\n');

        while (pEnd)
        {
            string strTemp;
            strTemp.insert(0, pBegin, pEnd-pBegin);
            //assert(!strTemp.empty());
            if(strTemp.empty()) break;
            if(m_rowHand != NULL)
            {
                vector<string> strVec;
                //assert(GetParamFromString(strTemp, strVec) > 0);
                if(GetParamFromString(strTemp, strVec) <= 0) break;
                m_rowHand(uiIndex,strVec);
            }
            else
            {
                stringMap[uiIndex] = strTemp;
            }
            uiIndex++;
            pBegin = pEnd + 1;
            pEnd = strchr(pBegin, '\n');
        }
        delete []fileBuffer;
        fileBuffer = NULL;
        pBegin = NULL;
        pEnd = NULL;
        fclose(pFile);

        if(m_rowHand == NULL)
        {
            map<u32, string>::iterator iter = stringMap.begin();
            for (; iter != stringMap.end(); ++iter)
            {
                vector<string> stringVec;
                map<u32, string> stringMapTemp;
                assert(GetParamFromString(iter->second, stringVec) > 0);

                vector<string>::size_type idx = 0;
                for (; idx != stringVec.size(); ++idx)
                {
                    stringMapTemp[idx + 1] = stringVec[idx];
                }

                m_stringMap[iter->first] = stringMapTemp;
            }
        }

        m_CSVName = path;
        return true;
    } 
    else
    {
        return false;
    }
}

bool CppCSV::SaveCSV(const char *path /* = NULL */)
{
    if (path != NULL)
    {
        m_CSVName = path;
    }

    FILE *pFile = fopen(m_CSVName.c_str(), "w");
    if (pFile)
    {
        map<u32, map<u32, string>>::iterator iter = m_stringMap.begin();
        for (; iter != m_stringMap.end(); ++iter)
        {
            map<u32, string> &rStringMap = iter->second;
            map<u32, string>::iterator it = rStringMap.begin();
            for (; it != rStringMap.end(); ++it)
            {
                string strTemp = it->second;
                strTemp += ',';
                fwrite(strTemp.c_str(), 1, 1, pFile);
            }

            char delim = '\n';
            fwrite(&delim, 1, 1, pFile);
        }

        fclose(pFile);
        return true;
    } 
    else
    {
        return false;
    }
}

bool CppCSV::GetIntValue(u32 uiRow, u32 uiCol, int &riValue)
{
    string *pStr = GetStringValue(uiRow, uiCol);
    if (pStr)
    {
        riValue = atoi(pStr->c_str());
        return true;
    } 
    else
    {
        return false;
    }
}

bool CppCSV::GetFloatValue(u32 uiRow, u32 uiCol, float &rfValue)
{
    string *pStr = GetStringValue(uiRow, uiCol);
    if (pStr)
    {
        rfValue = atof(pStr->c_str());
        return true;
    } 
    else
    {
        return false;
    }
}

string* CppCSV::GetStringValue(u32 uiRow, u32 uiCol)
{
    map<u32, map<u32, string>>::iterator iter = m_stringMap.find(uiRow);
    if (iter != m_stringMap.end())
    {
        map<u32, string> &rStrMap = iter->second;
        map<u32, string>::iterator it = rStrMap.find(uiCol);
        if (it != rStrMap.end())
        {
            return &(it->second);
        } 
        else
        {
            return NULL;
        }
    } 
    else
    {
        return NULL;
    }
}

//用于分割字符串，将CSV表格中的一行按照规则解析成一组字符串，存储在一个vector中
//根据CSV表格中所存储的数据的不同，重载各函数
int CppCSV::GetParamFromString(string str, vector<string> &stringVec, char delim)
{
    char *token = strtok(const_cast<char *>(str.c_str()), &delim);
    while (token)
    {
        string strTemp = token;
        stringVec.push_back(strTemp);
        token = strtok(NULL, &delim);
    }

    return stringVec.size();
}



UtilOper.hpp


#define _UtilOper_HPP_

#include "stdafx.h"
#include <math.h>
#include <string>

#include <windows.h>
#include <wchar.h>
using namespace std;

namespace UtilOper_hpp
{
    static time_t Convert_string_to_time_t(const std::string & time_string)
    {
        struct tm tm1;
        time_t time1;
        int i = sscanf(time_string.c_str(), "%d/%d/%d %d:%d:%d" ,    
            &(tm1.tm_year),
            &(tm1.tm_mon),
            &(tm1.tm_mday),
            &(tm1.tm_hour),
            &(tm1.tm_min),
            &(tm1.tm_sec),
            &(tm1.tm_wday),
            &(tm1.tm_yday));

        tm1.tm_year -= 1900;
        tm1.tm_mon --;
        tm1.tm_isdst=-1;
        time1 = mktime(&tm1);

        return time1;
    }

    static string&   replace_all(string&   str,const   string&   old_value,const   string&   new_value)   
    {   
        while(true)   {   
            string::size_type   pos(0);   
            if(   (pos=str.find(old_value))!=string::npos   )   
                str.replace(pos,old_value.length(),new_value);   
            else   break;   
        }   
        return   str;   
    }   
    static string&   replace_all_distinct(string&   str,const   string&   old_value,const   string&   new_value)   
    {   
        for(string::size_type   pos(0);   pos!=string::npos;   pos+=new_value.length())   {   
            if(   (pos=str.find(old_value,pos))!=string::npos   )   
                str.replace(pos,old_value.length(),new_value);   
            else   break;   
        }   
        return   str;   
    }
}
