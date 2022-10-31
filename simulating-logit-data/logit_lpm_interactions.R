require(ggplot2)
require(gridExtra)
require(grid)

set.seed(45683)

prob2logit <- function(x){
  logit = log(x / (1 - x))
}
intercept <- prob2logit(0.5)

#Simulate dummy x continuous
sim_dummy_cont = function(sample_size = 30000, beta_0 = intercept, beta_1 = -1.5, beta_2= 0.8, beta_3 = -0.8) {
  x1 = rnorm(n = sample_size)
  x2 = rbinom(n = sample_size, size = 1, prob = 0.7)
  eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * (x2 * x1)
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}

#Simulate dummy x dummy 
sim_dummy_dummy = function(sample_size = 30000, beta_0 = intercept, beta_1 = -1.5, beta_2= 0.8, beta_3 = -0.8) {
  x1 = rbinom(n = sample_size, size = 1, prob = 0.3)
  x2 = rbinom(n = sample_size, size = 1, prob = 0.7)
  eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * (x2 * x1)
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}

#simulate continuous x continuous
sim_cont_cont = function(sample_size = 300000, beta_0 = intercept, beta_1 = -1.5, beta_2= 0.8, beta_3 = -0.8) {
  x1 = rnorm(n = sample_size)
  x2 = rnorm(n = sample_size)
  eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * (x2 * x1)
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}


#Simulate data
data = sim_dummy_cont()

#Dummy x cont
logit <- glm(y ~ x1 + x2 + (x2*x1), data = data,  family=binomial(link='logit'))
pred_logit <- data.frame(unlist(logit$fitted.values), unlist(data$x1), unlist(as.factor(data$x2)))
names(pred_logit) = c("pred","x1", "x2")

p1 <- ggplot(pred_logit, aes(x=x1, y=pred, color=x2)) + 
      geom_line() +
      scale_color_manual(values=c('red','blue')) +
      ggtitle("Logistic regression") +
      theme(plot.title = element_text(hjust = 0.5))+
      theme(legend.position="top")+ 
      ylab("Predicted probability")

#Run LPM
lpm <- lm(y ~ x1 + x2 + (x2*x1), data = data)
pred_lpm <- data.frame(unlist(lpm$fitted.values), unlist(data$x1), unlist(as.factor(data$x2)))
names(pred_lpm) = c("pred","x1", "x2")

p2 <- ggplot(pred_lpm, aes(x=x1, y=pred, color=x2)) + 
      geom_line() +
      scale_color_manual(values=c('red','blue')) +
      ggtitle("LPM") +
      theme(plot.title = element_text(hjust = 0.5)) +
      theme(legend.position="top")+ 
      ylab("Predicted probability")

grid.arrange(p1, p2, ncol =2, top = textGrob("Dummy * Continuous Interaction Effect", 
                                             gp=gpar(fontsize=15)))


#Simulate dummy x dummy 
data = sim_dummy_dummy()
logit <- glm(y ~ x1 + x2 + (x2*x1), data = data,  family=binomial(link='logit'))
pred_logit <- data.frame(unlist(logit$fitted.values), unlist(data$x1), unlist(as.factor(data$x2)))
names(pred_logit) = c("pred","x1", "x2")
lpm <- lm(y ~ x1 + x2 + (x2*x1), data = data)
pred_lpm <- data.frame(unlist(lpm$fitted.values), unlist(data$x1), unlist(as.factor(data$x2)))
names(pred_lpm) = c("pred","x1", "x2")

p3 <- ggplot(pred_logit, aes(x=x1, y=pred, color=x2)) + 
  geom_line() +
  scale_color_manual(values=c('red','blue')) +
  ggtitle("Logistic Regression")+
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability")


p4 <- ggplot(pred_lpm, aes(x=x1, y=pred, color=x2)) + 
  geom_line() +
  scale_color_manual(values=c('red','blue')) +
  ggtitle("LPM")+
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability")

grid.arrange(p3, p4, ncol =2, top = textGrob("Dummy * Dummy Interaction Effect", 
                                             gp=gpar(fontsize=15)))


#Simulate cont x cont 
data = sim_cont_cont()
logit <- glm(y ~ x1 + x2 + (x2*x1), data = data,  family=binomial(link='logit'))
pred_logit <- data.frame(unlist(logit$fitted.values), unlist(data$x1), unlist(data$x2))
names(pred_logit) = c("pred","x1", "x2")
lpm <- lm(y ~ x1 + x2 + (x2*x1), data = data)
pred_lpm <- data.frame(unlist(lpm$fitted.values), unlist(data$x1), unlist(data$x2))
names(pred_lpm) = c("pred","x1", "x2")

p5 <- ggplot(pred_logit, aes(x=x1, y=pred, color = x2)) + 
  geom_point() +
  ggtitle("Logistic Regression") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability")

p6 <- ggplot(pred_lpm, aes(x=x1, y=pred, color = x2)) + 
  geom_point() +
  ggtitle("LPM") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability")


grid.arrange(p5, p6, ncol =2,top = textGrob("Continuous * Continuous Interaction Effect", 
                                            gp=gpar(fontsize=15)))