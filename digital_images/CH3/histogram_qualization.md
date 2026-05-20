# 直方圖均化演算法 公式

#  Step 1: Compute the histogram of input image  
$$P_r(r_k) = \frac{n_k}{n}, \quad k = 0, 1, \dots, L-1$$

#  Step 2: Compute the transformation function  
$$s_k = T(r_k) = (L-1) \sum_{j=0}^{k} P_r(r_j)$$

#  Transform the value of each pixel   
$$f(x, y)_{new} = \text{round}(s_{f(x, y)_{old}})$$