from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Category, Comment
from user.models import User
from .serializers import PostSerializer, CommentSerializer

class PostAPI(APIView):
    # Post 작성 (Create)
    # request = [title, content]
    def post(self, request):
        # 빈 Post 객체 생성
        post = Post()

        # request에 있는 데이터를 빈 Post 객체에 저장
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.writer = request.user # 현재 로그인 중인 유저
        post.save()

        # Serializer를 이용해서 post의 정보를 JSON으로 변환해서 반환
        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, status=200)   
    
    # Post 조회 (Read)
    def get(self, request):
        # 모든 Post 저장
        posts = Post.objects.all()
        
        # Serializer를 이용해서 JSON으로 변환
        postSerializer = PostSerializer(posts, many=True) # 대상이 여러 개면 many=True
        return Response(postSerializer.data, status=200)   
    
    # Post 수정 (Update)
    # request = [id, title, content]
    def put(self, request):
        
        # id로 Post 조회
        post = Post.objects.filter(id = request.data[id])

        # 데이터 수정
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.save()

        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, status=200)    
    
    # Post 삭제 (Update)
    # request = [id]
    def delete(self, request):

        # id로 Post 조회
        post = Post.objects.filter(id = request.data[id])

        # 삭제
        post.delete()
        
        return Response(status=200)
    
# 설명 생략 RUD 생략
class CommentAPI(APIView):
    def post(self, request):
        comment = Comment()
        comment.content = request.data["content"]
        comment.writer = request.user
        comment.save()

        return Response(status=200)


        
# ------------ 여기서부터 과제 정답 ------------
# 카테고리를 이름으로 받는다고 가정했습니다!! id로 받아와도 OK
# 코드에 정답은 없습니다~~~ 결과만 정확하면 다 정답이에요

# 1. '카테고리별' 게시글 작성
class Q1(APIView):
    # request = [title, content, category]
    def post(self, request):
        post = Post()

        post.title = request.data["title"]
        post.content = request.data["content"]
        post.writer = request.user
        
        # 존재하는 Category일 때
        if (Category.objects.filter(name = request.data["category"])):
            # 일치하는 Category를 찾아서 post에 저장
            post.category = Category.objects.get(name = request.data["category"])
        
        # 존재하지 않는 Category일 때
        else:
            # 새로운 Category를 만들어서 post에 저장
            category = Category()
            category.name = request.data["category"]
            category.save()

            post.category = category

        post.save()

        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, status=200)   

# 2. '카테고리별' 게시글 조회
class Q2(APIView):
    # request = [category]
    def get(self, request):
        # Category 이름으로 조회
        categoryObj = Category.objects.get(name = request.data["category"])

        # Category가 일치하는 Post 조회
        posts = Post.objects.filter(category = categoryObj)
        
        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data, status=200) 

# 3. '내'가 작성한 게시글 조회
class Q3(APIView):
    def get(self, request):
        posts = Post.objects.filter(writer = request.user)

        postSerializer = PostSerializer(posts, many=True)
        return Response(postSerializer.data, status=200) 

# 4. '내'가 작성한 댓글 조회
class Q4(APIView):
    def get(self, request):
        comments = Comment.objects.filter(writer = request.user)

        commentSerializer = CommentSerializer(comments, many=True)
        return Response(commentSerializer.data, status=200)
    
# 5. '특정 유저'가 작성한 댓글 조회
class Q5(APIView):
    # request = [(user)id]
    def get(self, request):
        user = User.objects.get(id = request.data["id"])
        comments = Comment.objects.filter(writer = user)
        commentSerializer = CommentSerializer(comments, many=True)
        return Response(commentSerializer.data, status=200)

# 6. 게시글 좋아요 기능
class Q6(APIView):
    # request = [(post)id]
    def post(self, request):
        post = Post.objects.get(id = request.data["id"])

        # 이미 눌렀으면 취소
        if request.user in post.like.all():
            post.like.remove(request.user)
        
        # 안 눌렀으면 추가
        else:
            post.like.add(request.user)

        # 현재 좋아요 개수 반환
        return Response({"message": post.like.count()})





