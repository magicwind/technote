---
layout: post
title:  "归并排序的Java实现"
categories: algorithm
---
## 简介
归并排序（Merge Sort）是将两个（或两个以上）有序表合并成一个新的有序表，即把待排序序列分为若干个子序列，每个子序列是有序的。
然后再把有序子序列合并为整体有序序列。

归并排序是建立在归并操作上的一种有效的排序算法。
该算法是采用分治法（Divide and Conquer）的一个非常典型的应用。

将已有序的子序列合并，得到完全有序的序列；即先使每个子序列有序，再使子序列段间有序。若将两个有序表合并成一个有序表，称为2-路归并。

归并排序算法稳定，数组需要O(n)的额外空间，链表需要O(log(n))的额外空间，时间复杂度为O(nlog(n))，算法不是自适应的，不需要对数据的随机读取。

## 归并的工作原理
1. 申请空间，使其大小为两个已经排序序列之和，该空间用来存放合并后的序列
2. 设定两个指针，最初位置分别为两个已经排序序列的起始位置
3. 比较两个指针所指向的元素，选择相对小的元素放入到合并空间，并移动指针到下一位置
4. 重复步骤3直到某一指针达到序列尾
5. 将另一序列剩下的所有元素直接复制到合并序列尾

## 代码演示
{% highlight java %}
public class MergeSort {

    public static void main(String[] args) {
        int[] sortArray = new int[] { 5, 3, 6, 2, 1, 9, 4, 8, 7 };
        System.out.println("待排序的数组：");
        print(sortArray);

        int[] sortedArray = mergeSort(sortArray);

        System.out.println("排序后的数组：");
        print(sortedArray);
    }

    private static int[] mergeSort(int[] sortArray) {
        sort(sortArray, 0, sortArray.length - 1);

        return sortArray;
    }

    private static void sort(int[] sortArray, int start, int end) {
        if (start < end) {
            // 找出中间索引  
            int middle = (end - start) / 2 + start;
            // 对左边数组进行递归  
            sort(sortArray, start, middle);
            // 对右边数组进行递归  
            sort(sortArray, middle + 1, end);
            // 归并  
            merge(sortArray, start, middle, end);

            System.out.print("merged: ");
            print(sortArray);
        }
    }

    private static void merge(int[] sortArray, int left, int middle, int right) {
        // 记录左边指针位置
        int leftPointer = left;
        // 记录右边指针位置
        int rightPointer = middle + 1;
        // 临时数组储存结果
        int[] tempArray = new int[right - left + 1];
        int tempArrayIndex = 0;

        // 从两个数组中取出最小的放入临时数组
        while (leftPointer <= middle && rightPointer <= right) {
            if (sortArray[leftPointer] <= sortArray[rightPointer]) {
                tempArray[tempArrayIndex++] = sortArray[leftPointer];
                leftPointer++;
            } else {
                tempArray[tempArrayIndex++] = sortArray[rightPointer];
                rightPointer++;
            }
        }

        // 剩余部分依次放入临时数组（实际上两个while只会执行其中一个）  
        while (leftPointer <= middle) {
            tempArray[tempArrayIndex++] = sortArray[leftPointer++];
        }

        while (rightPointer <= right) {
            tempArray[tempArrayIndex++] = sortArray[rightPointer++];
        }

        // 将临时数组中的内容拷贝回原数组中  
        for (int i = 0; i < tempArray.length; i++) {
            sortArray[left] = tempArray[i];
            left++;
        }
    }

    public static void print(int[] data) {  
        for (int i = 0; i < data.length; i++) {  
            System.out.print(data[i] + "\t");  
        }  
        System.out.println();  
    }  
}
{% endhighlight %}

运行结果：
{% highlight txt %}
待排序的数组：
5   3   6   2   1   9   4   8   7
merged: 3   5   6   2   1   9   4   8   7
merged: 3   5   6   2   1   9   4   8   7
merged: 3   5   6   1   2   9   4   8   7
merged: 1   2   3   5   6   9   4   8   7
merged: 1   2   3   5   6   4   9   8   7
merged: 1   2   3   5   6   4   9   7   8
merged: 1   2   3   5   6   4   7   8   9
merged: 1   2   3   4   5   6   7   8   9
排序后的数组：
1   2   3   4   5   6   7   8   9
{% endhighlight %}