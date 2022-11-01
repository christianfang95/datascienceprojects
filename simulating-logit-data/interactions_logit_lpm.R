require(ggplot2)
require(gridExtra)
require(grid)

set.seed(45683)

prob2logit <- function(x){
  logit = log(x / (1 - x))
}


intercept <- prob2logit(0.5)

#Simulate dummy x continuous
sim_dummy_cont = function(sample_size = 3000, beta_0 = intercept, beta_1 = -1.5, beta_2= 0.8, beta_3 = -0.4) {
  x1 = rnorm(n = sample_size)
  x2 = rbinom(n = sample_size, size = 1, prob = 0.7)
  eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * (x2 * x1)
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}

#Simulate dummy x dummy 
sim_dummy_dummy = function(sample_size = 3000, beta_0 = intercept, beta_1 = +1.5, beta_2= +0.8, beta_3 = -0.6) {
  x1 = rbinom(n = sample_size, size = 1, prob = 0.3)
  x2 = rbinom(n = sample_size, size = 1, prob = 0.7)
  eta = beta_0 + beta_1 * x1+ beta_2 * x2 + beta_3 * (x2 * x1)
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}

#simulate continuous x continuous
sim_cont_cont = function(sample_size = 3000, beta_0 = intercept, beta_1 = -0.5, beta_2= 0.8, beta_3 = -0.8) {
  x1 = rnorm(n = sample_size)
  x2 = sample(rep(1:5, each = (sample_size/5)))
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
      scale_color_manual(values=c('#74a9cf','#034e7b'), labels = c("rural", "urban")) +
      ggtitle("Logistic regression") +
      theme(plot.title = element_text(hjust = 0.5))+
      theme(legend.position="top")+ 
      ylab("Predicted probability of renting") +
      xlab("Wealth")


#Run LPM
lpm <- lm(y ~ x1 + x2 + (x2*x1), data = data)
pred_lpm <- data.frame(unlist(lpm$fitted.values), unlist(data$x1), unlist(as.factor(data$x2)))
names(pred_lpm) = c("pred","x1", "x2")

p2 <- ggplot(pred_lpm, aes(x=x1, y=pred, color=x2)) + 
      geom_line() +
      scale_color_manual(values=c('#74a9cf','#034e7b'), labels = c("rural", "urban")) +
      ggtitle("LPM") +
      theme(plot.title = element_text(hjust = 0.5)) +
      theme(legend.position="top")+ 
      ylab("Predicted probability of renting") +
      xlab("Wealth") 

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
  geom_point() +
  scale_color_manual(values=c('#74a9cf','#034e7b'), labels = c("rural", "urban")) +
  ggtitle("Logistic Regression")+
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability of renting")+
  xlab("Unemployed") +
  scale_x_discrete(limits = c(0,1), labels=c("0" = "0: Working", "1" = "1: Unemployed"))+
  ylim(0,1)


p4 <- ggplot(pred_lpm, aes(x=x1, y=pred, color=x2)) + 
  geom_point() +
  scale_color_manual(values=c('#74a9cf','#034e7b'), labels = c("rural", "urban")) +
  ggtitle("LPM")+
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("PPredicted probability of renting") +
  xlab("Unemployed")+
  scale_x_discrete(limits = c(0,1), labels=c("0" = "0: Working", "1" = "1: Unemployed")) +
  ylim(0,1)

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

p5 <- ggplot(pred_logit, aes(x=x1, y=pred, color = as.factor(x2))) + 
  #geom_point()+
  geom_line(size = 1) +
  ggtitle("Logistic Regression") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability of renting")+
  xlab("Wealth") +
  labs(colour = "Happiness") +
  scale_color_discrete(type=c( '#a6bddb', '#74a9cf', '#2b8cbe', '#045a8d', '#034e7b'))

p6 <- ggplot(pred_lpm, aes(x=x1, y=pred, color = as.factor(x2))) + 
  geom_line(size=1) +
  ggtitle("LPM") +
  theme(plot.title = element_text(hjust = 0.5)) +
  theme(legend.position="top")+ 
  ylab("Predicted probability of renting")+
  xlab("Wealth") +
  labs(colour = "Happiness") +
  scale_color_discrete(type=c( '#a6bddb', '#74a9cf', '#2b8cbe', '#045a8d', '#034e7b'))



grid.arrange(p5, p6, ncol =2,top = textGrob("Continuous * Continuous Interaction Effect", 
                                            gp=gpar(fontsize=15)))

