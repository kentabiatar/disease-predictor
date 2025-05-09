# -*- coding: utf-8 -*-



"""# Prediction using XGBoost

## Model Defining and Training
"""

model = XGBClassifier(eval_metric='merror', max_depth = 6, gamma = 0, min_child_weight = 6, n_estimators = 177, learning_rate = 0.01)

model.fit(X_train_smote, y_train_smote, eval_set=[(X_train_smote, y_train_smote), (X_test, y_test)], verbose=False)

joblib.dump(X_final.columns.tolist(), "feature_columns.pkl")
joblib.dump(y_encoder, "label_encoder.pkl")
joblib.dump(model, 'xgboost_model.pkl')

predicted = model.predict(X_test)

"""## Model Evaluation"""

accuracy_score(predicted, y_test)

print(classification_report(y_test, predicted, target_names=y_encoder.classes_))

cm = confusion_matrix(predicted, y_test)
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=y_encoder.classes_,
            yticklabels=y_encoder.classes_)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

results = model.evals_result()
plt.plot(results['validation_0']['merror'], label='Train')
plt.plot(results['validation_1']['merror'], label='Test')
plt.xlabel("Rounds")
plt.ylabel("Multiclass Error")
plt.title("XGBoost Learning Curve")
plt.legend()

booster = model.get_booster()
plt.figure(figsize=(30, 20))
plot_tree(model, num_trees=1)

# To save the plot as a file
fig = plt.gcf()
fig.set_size_inches(30, 15)
fig.savefig("xgb_tree_21.png")

plt.show()

tree_dot = to_graphviz(model, num_trees=2)
# Save the dot file
dot_file_path = "xgboost_tree.dot"
tree_dot.save(dot_file_path)
# Convert dot file to png and display
with open(dot_file_path) as f:
    dot_graph = f.read()
# Use graphviz to display the tree
graph = graphviz.Source(dot_graph)
graph.render("xgboost_tree")
# Optionally, visualize the graph directly


plot_importance(booster, height=2)
plt.show()

"""# Model Utilization"""
probas = model.predict_proba(X_test)
class_names = y_encoder.classes_
top3_list = []
for i in range(len(X_test)):
    top3_idx = np.argsort(probas[i])[-3:][::-1]
    top3_diseases = class_names[top3_idx]
    top3_probs = probas[i][top3_idx]
    top3_list.append({
        'Patient_Index': i,
        'Top_1': f"{top3_diseases[0]} ({top3_probs[0]*100:.2f}%)",
        'Top_2': f"{top3_diseases[1]} ({top3_probs[1]*100:.2f}%)",
        'Top_3': f"{top3_diseases[2]} ({top3_probs[2]*100:.2f}%)"
    })

top3_df = pd.DataFrame(top3_list)
top3_df.head(20)

