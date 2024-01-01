from django.shortcuts import render 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import itertools
import json
# Create your views here.
def home(request):
    return render(request, "pages/home.html", {})
@csrf_exempt
def map(request):
    if request.method == 'POST':
        # Assuming the data is sent as JSON
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            checked_checkboxes = request_data.get('checkedCheckboxes', [])  
            ## args
            start = 0
            end = 13
            graph = [[0, 1.19, 2.41, 3.71, 4.49, 6.19, 2.31, 3.75, 4.93, 6.89, 7.38, 5.31, 8.64, 4.09], 
                     [1.19, 0, 1.22, 2.52, 3.75, 4.97, 1.34, 2.56, 3.86, 5.09, 6.41, 4.12, 7.45, 2.90], 
                     [2.41, 1.22, 0, 1.30, 2.53, 3.75, 2.56, 1.39, 2.69, 3.92, 5.24, 2.95, 6.23, 2.44], 
                     [3.71, 2.52, 1.30, 0, 1.23, 2.45, 3.74, 2.52, 1.22, 2.45, 3.77, 2.78, 4.93, 2.44], 
                     [4.49, 3.75, 2.53, 1.23, 0, 1.22, 5.73, 4.51, 3.21, 1.98, 2.44, 3.58, 3.70, 3.67], 
                     [6.19, 4.97, 3.75, 2.45, 1.22, 0, 6.30, 5.07, 3.77, 2.54, 1.22, 4.14, 2.48, 4.89], 
                     [2.32, 1.34, 2.56, 3.74, 5.73, 6.30, 0, 1.22, 2.52, 3.75, 5.07, 2.78, 8.79, 4.24], 
                     [3.75, 2.56, 1.39, 2.52, 4.51, 5.07, 1.22, 0, 1.30, 2.53, 3.85, 1.56, 7.55, 3.83], 
                     [4.93, 3.86, 2.69, 1.22, 3.21, 3.77, 2.52, 1.30, 0, 1.23, 2.55, 1.56, 6.25, 3.66], 
                     [6.89, 5.09, 3.92, 2.45, 1.98, 2.54, 3.75, 2.53, 1.23, 0, 1.32, 1.60, 5.02, 5.65], 
                     [7.38, 6.41, 5.24, 3.77, 2.44, 1.22, 5.07, 3.85, 2.55, 1.32, 0, 2.92, 3.70, 6.11], 
                     [5.31, 4.12, 2.95, 2.78, 3.58, 4.14, 2.78, 1.56, 1.56, 1.60, 2.92, 0, 6.62, 5.22], 
                     [8.64, 7.45, 6.23, 4.93, 3.70, 2.48, 8.79, 7.55, 6.25, 5.02, 3.70, 6.62, 0, 7.37], 
                     [4.09, 2.90, 2.44, 2.44, 3.67, 4.89, 4.24, 3.83, 3.66, 5.65, 6.11, 5.22, 7.37, 0]]

            ## code start here
            marketList = ['start','Snaks','Hot Food','Bakery','Coffe/Hot Drinks','Fresh and Chilled Food','Accessories/Headwear','Shirts','Outerware','Novels/Magazzine','Energy Drinks/Wine/Beer','Cold Pressed Juice/Water','ATM','Cashier']
            shopping_list= []
            pre_shopping_list = checked_checkboxes
            for i in pre_shopping_list:
                shopping_list.append(marketList.index(i))

            n = len(graph)

            # Create a memoization table
            memo = {}

            # Initialize memoization table for the base case (no nodes visited)
            for last_node in range(n):
                if last_node != start:
                    memo[(1 << last_node, last_node)] = (graph[start][last_node], [start, last_node])

            # Iterate over all subsets of nodes (excluding the start and end nodes)
            for subset_size in range(2, len(shopping_list) + 1):
                for subset in itertools.combinations(shopping_list, subset_size):
                    subset_mask = sum(1 << node for node in subset)

                    for last_node in subset:
                        if last_node != start and last_node != end:
                            # If last_node is in the subset, update the minimum distance and route
                            for next_node in subset:
                                if next_node != last_node:
                                    new_subset_mask = subset_mask ^ (1 << last_node)
                                    if (new_subset_mask, next_node) in memo:
                                        distance = memo[(new_subset_mask, next_node)][0] + graph[next_node][last_node]
                                        route = memo[(new_subset_mask, next_node)][1] + [last_node]
                                        if (subset_mask, last_node) not in memo or distance < memo[(subset_mask, last_node)][0]:
                                            memo[(subset_mask, last_node)] = (distance, route)

            # Find the optimal route from start to end
            optimal_distance = float('inf')
            optimal_route = None
            subset_mask = sum(1 << node for node in shopping_list)
            for node in shopping_list:
                if node != end:
                    distance, route = memo[(subset_mask, node)]
                    distance += graph[node][end]
                    if distance < optimal_distance:
                        optimal_distance = distance
                        optimal_route = route + [end]

            final_route = []
            for j in optimal_route:
                final_route.append(j)
           
            # Perform operations on the data
            result = final_route
            # Return a JSON response
            return JsonResponse({'result': result})
        except Exception as e:
            # Handle exceptions, e.g., invalid JSON format
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Invalid method'}, status=405)
 