import json
from math import sqrt

file = open('datas/shopping_trends.json')
shoppingTrendData = json.load(file)

file2 = open('datas/movie_likeds.json')
movieData = json.load(file2)


class KNNRecommenderFilter:
    def __init__(self, dataSet, resultCount, algorithmType):
        self.dataSet = dataSet
        self.resultCount = resultCount
        self.algorithmType = algorithmType

    def recommendList(self, data_item):
        neighbors = self.find_near_neighbors(data_item)
        recommendations = {}
        data = self.dataSet[data_item]
        total_distance = 0.0

        for i in range(self.resultCount):
            total_distance += neighbors[i][0]

        for i in range(self.resultCount):
            selected_data_row = neighbors[i][1]
            selected_data = self.dataSet[selected_data_row]
            if total_distance != 0:
                weight = neighbors[i][0] / total_distance
            else:
                weight = 0

            for product in selected_data:
                if data[product] == 0.0:
                    if not product in recommendations:
                        recommendations[product] = selected_data[product] * weight
                    else:
                        recommendations[product] = recommendations[product] + selected_data[product] * weight

        recommendations = sorted(recommendations.items(), key=lambda list: list[1], reverse=True)

        print('----------------------------------------------------')
        print('Recommendations List\n')
        if len(recommendations) < self.resultCount:
            for i in range(len(recommendations)):
                if recommendations[i][1] != 0:
                    print(' ==> '+recommendations[i][0])
        else:
            for i in range(self.resultCount):
                if recommendations[i][1] != 0:
                    print(' ==> '+recommendations[i][0])

    def similarity_algorithm(self, type, selectedRowData, rowData):
        if type > 2 or type < 1:
            type = 2
        if type == 1:
            result = self.manhattan_method(selectedRowData, rowData)
        elif type == 2:
            result = self.cosine_similarity_method(selectedRowData, rowData)
        return result

    def find_near_neighbors(self, data_item):
        distances = []
        for oneData in self.dataSet:
            if oneData != data_item:
                distance = self.similarity_algorithm(self.algorithmType, self.dataSet[oneData],
                                                     self.dataSet[data_item])
                distances.append((distance, oneData))
        distances = sorted(distances, key=lambda list: list[0], reverse=False)
        return distances

    def manhattan_method(self, rating1, rating2):
        distance = 0
        for key in rating1:
            if key in rating2:
                distance += abs(rating1[key] - rating2[key])
        return distance

    def cosine_similarity_method(self, rating1, rating2):
        zigma_x2 = 0
        zigma_y2 = 0

        for oneRate in rating1:
            zigma_x2 = zigma_x2 + rating1[oneRate] * rating1[oneRate]
        sum_x2_sqrt = sqrt(zigma_x2)

        for oneRate in rating2:
            zigma_y2 = zigma_y2 + rating2[oneRate] * rating2[oneRate]
        sum_y2_sqrt = sqrt(zigma_y2)

        multi = 0
        for product in rating1:
            if product in rating2:
                multi = multi + rating2[product] * rating1[product]

        distance = multi / (sum_x2_sqrt * sum_y2_sqrt)
        distance = distance * -1
        return distance



print('\n')
print('Data Set List\n')
print('=> Shopping Trends Turkey | Data Id : 1')
print('=> Movie Liked | Data Id : 2')
select_data_id = int(input('\n====> Please to Enter Dataset ID : '))
print('\n')
print('Method List For KNN\n')
print('=> Manhattan Distance Method | Type Id : 1')
print('=> Cosine Similarity Distance Method | Type Id : 2')
method_type_id = int(input('\n====> Please Choose Method For KNN | Type Id : '))
recommend_count = int(input('\n====> Please Enter For Recommend Count (min:1 | max:10) : '))
if recommend_count > 10:
    recommend_count = 10
elif recommend_count == 0:
    recommend_count = 1

if select_data_id == 1:
    KNNRecommenderFilter(shoppingTrendData, recommend_count, method_type_id).recommendList("data0")
elif select_data_id == 2:
    KNNRecommenderFilter(movieData, recommend_count, method_type_id).recommendList("movie0")
