pipeline {
    agent any
    
    tools {
        python 'Python3'  // 需要在 Jenkins 全局工具配置中配置 Python
    }
    
    environment {
        // 定义环境变量
        BASE_URL = 'https://xue.yunvip123.com'
        TEST_REPORTS_DIR = './reports'
        SCREENSHOTS_DIR = './screenshots'
    }
    
    stages {
        stage('清理工作空间') {
            steps {
                cleanWs()
            }
        }
        
        stage('拉取代码') {
            steps {
                checkout scm
            }
        }
        
        stage('安装依赖') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        
        stage('运行自动化测试') {
            steps {
                script {
                    // 运行冒烟测试
                    sh 'python -m pytest testcases/ -m smoke -v --alluredir=${TEST_REPORTS_DIR}/allure-results'
                    
                    // 运行所有测试（可选）
                    // sh 'python -m pytest testcases/ -v --alluredir=${TEST_REPORTS_DIR}/allure-results'
                }
            }
            post {
                always {
                    // 保存测试报告
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: "${TEST_REPORTS_DIR}/allure-results"]]
                    ])
                    
                    // 保存截图
                    archiveArtifacts artifacts: "${SCREENSHOTS_DIR}/**/*.png", allowEmptyArchive: true
                }
            }
        }
        
        stage('生成测试报告') {
            steps {
                script {
                    sh 'allure generate ${TEST_REPORTS_DIR}/allure-results -o ${TEST_REPORTS_DIR}/allure-report --clean'
                }
            }
            post {
                always {
                    // 发布 HTML 报告
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: "${TEST_REPORTS_DIR}/allure-report",
                        reportFiles: 'index.html',
                        reportName: 'Allure 测试报告'
                    ])
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ 测试执行成功！'
        }
        failure {
            echo '❌ 测试执行失败！'
            // 发送失败通知（可选）
            // emailext (
            //     subject: "构建失败: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            //     body: "构建失败，请查看报告: ${env.BUILD_URL}",
            //     to: "your-email@example.com"
            // )
        }
        always {
            echo "构建完成: ${env.BUILD_URL}"
        }
    }
}