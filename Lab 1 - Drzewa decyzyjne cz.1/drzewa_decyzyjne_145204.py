# -*- coding: utf-8 -*-
"""Drzewa_decyzyjne_145204.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zVJvW8amqPtN27rWT1TrmRivSFWWjm-t
"""

import pandas as pd
import numpy as np
import json
import pydot
import uuid
from skimage import io

def read_data():
  data = pd.read_csv('titanic-homework.csv')
  data = data.drop(columns=['PassengerId', 'Name'])
  for i in data['Age']:
    if i <= 20:
      data['Age'] = data['Age'].replace([i], "young (0-20)")
    elif i > 20 and i <= 40:
      data['Age'] = data['Age'].replace([i], "middle (21-40)")
    else:
      data['Age'] = data['Age'].replace([i], "old (41-100)")
  return data

def calculate_total_entropy(data, label):
  data_size = data.shape[0]
  partial_entropies = []
  for i in np.unique(data[label]):
    label_class_count = data[data[label] == i].shape[0]
    partial_entropies.append((label_class_count/data_size)*np.log2(label_class_count/data_size))
  return -sum(partial_entropies)

def calculate_entropy(filtered_data, label):
  filtered_data_size = filtered_data.shape[0]
  partial_entropies = []
  for i in np.unique(filtered_data["Survived"]):
    label_class_count = filtered_data[filtered_data[label] == i].shape[0]
    if label_class_count == 0:
      partial_entropies.append(0)
    else:
      partial_entropies.append((label_class_count/filtered_data_size)*np.log2(label_class_count/filtered_data_size))
  return -sum(partial_entropies)

def calculate_conditional_entropy(feature, data, label):
  feature_values = data[feature].unique()
  data_size = data.shape[0]
  conditional_entropies_parts = []
  for feature_value in feature_values:
    feature_value_data = data[data[feature] == feature_value]
    feature_value_count = feature_value_data.shape[0]
    feature_value_entropy = calculate_entropy(feature_value_data, label)
    feature_value_probability = feature_value_count/data_size
    conditional_entropies_parts.append(feature_value_probability * feature_value_entropy)

  return sum(conditional_entropies_parts)

def calculate_gain(feature, data, label):
  return calculate_total_entropy(data, label) - calculate_conditional_entropy(feature, data, label)

def find_best_feature(data, label):
  features = data.drop(columns = [label])

  features_info_gains = dict()

  for feature in features:
    features_info_gains[feature] = calculate_gain(feature, data, label)
  
  return max(features_info_gains, key=features_info_gains.get)

def perform_split(feature, data, label):
  feature_values = data[feature].value_counts(sort=False)
  tree = dict()

  for feature_value, count in feature_values.items():
    feature_value_data = data[data[feature] == feature_value]

    pure_node = False
    for i in np.unique(data[label]):
      class_count = feature_value_data[feature_value_data[label] == i].shape[0]

      if class_count == count:
        tree[feature_value] = i
        data = data[data[feature] != feature_value]
        pure_node = True

    if not pure_node:
      tree[feature_value] = "?"
    
  return tree, data

def build_tree(data, label, root, previous_feature):
  if data.shape[0] != 0:
    best_feature = find_best_feature(data, label)
    tree, data = perform_split(best_feature, data, label)
    next_root = None

    if previous_feature != None:
      root[previous_feature] = dict()
      root[previous_feature][best_feature] = tree
      next_root = root[previous_feature][best_feature]
    else:
      root[best_feature] = tree
      next_root = root[best_feature]
    
    for node, branch in list(next_root.items()):
      if branch == "?":
        feature_value_data = data[data[best_feature] == node]
        build_tree(feature_value_data, label, next_root, node)

def id3(data, label):
  tree = dict()
  build_tree(data, label, tree, None)
  return tree

def predict(tree, instance):
  if not isinstance(tree, dict):
      return tree
  else:
      root_node = next(iter(tree))
      feature_value = instance[root_node]
      if feature_value in tree[root_node]:
          return predict(tree[root_node][feature_value], instance)
      else:
          return None

def evaluate(tree, test_data, label):
  correct_predict = 0
  wrong_predict = 0
  y_predicted = []
  y_test = []
  for i in range(test_data.shape[0] - 1):
    result = predict(tree, test_data.iloc[i])
    y_predicted.append(result)
    y_test.append(test_data[label].iloc[i])
    if result == test_data[label].iloc[i]:
        correct_predict += 1
    else:
        wrong_predict += 1
  accuracy = correct_predict / (correct_predict + wrong_predict)

  #print(correct_predict)
  #print(wrong_predict)
  #print(y_predicted)
  #print(y_test)
  #conf_matrix = {'y_actual': y_test, 'y_predicted': y_predicted}

  #df = pd.DataFrame(conf_matrix)

  #confusion_matrix = pd.crosstab(df['y_actual'], df['y_predicted'], rownames=['Actual'], colnames=['Predicted'])
  #print(confusion_matrix)

  print("Accuracy: " + str(round(accuracy, 4) * 100) + "%")

class NpEncoder(json.JSONEncoder):
  def default(self, obj):
      if isinstance(obj, np.integer):
          return int(obj)
      if isinstance(obj, np.floating):
          return float(obj)
      if isinstance(obj, np.ndarray):
          return obj.tolist()
      return super(NpEncoder, self).default(obj)

def create_graph(graph, dictionary, parent_node=None):
  for key in dictionary.keys():
      if parent_node is not None:
          from_name = parent_node.get_name().replace("\"", "") + '_' + str(key)
          from_label = str(key)
          obj_dict = {}
          node_from = pydot.Node(from_name, label=from_label)
          graph.add_node(node_from)
          graph.add_edge( pydot.Edge(parent_node, node_from) )
          if isinstance(dictionary[key], dict):
              create_graph(graph, dictionary[key], node_from)
          else:
              to_name = str(uuid.uuid4()) + '_' + str(dictionary[key])
              to_label = str(dictionary[key])
              node_to = pydot.Node(to_name, label=to_label, shape='box')
              graph.add_node(node_to)
              graph.add_edge(pydot.Edge(node_from, node_to))
      else:
          from_name =  str(key)
          from_label = str(key)
          node_from = pydot.Node(from_name, label=from_label)
          create_graph(graph, dictionary[key], node_from)

def plot_tree(tree, name):
  graph = pydot.Dot(graph_type='graph')
  create_graph(graph, tree)
  graph.write_png(name+'.png')

data = read_data()
data = data.astype(str)

mask = np.random.rand(len(data)) < 0.66
train_data = data[mask]
test_data = data[~mask]

#from sklearn.model_selection import train_test_split
#train_data, test_data = train_test_split(data, test_size=0.25)
#print(train_data)
#print(test_data)

label = "Survived"
tree = id3(train_data, label)

#print(json.dumps(tree, indent = 4, sort_keys=False, cls=NpEncoder))
plot_tree(tree,'1')

evaluate(tree, test_data, label)

#Accuracies:
#89.66%
#85.71%
#80.00%
#91.88%
#90.62%
#86.21%
#80.65%