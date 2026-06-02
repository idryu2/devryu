import { useState } from 'react'
import Header from './components/Header.jsx'
import BlogSection from './components/blog/BlogSection.jsx'
import { initialPosts } from './data/posts.js'
import './styles/app.css'

export default function App() {
  // 블로그 글 데이터는 App에서 관리해 다른 영역에서도 재사용할 수 있게 둔다.
  const [posts, setPosts] = useState(initialPosts)

  const addPost = (post) => {
    setPosts((prev) => [
      {
        id: Date.now(),
        date: new Date().toISOString().slice(0, 10),
        views: 0,
        ...post,
      },
      ...prev,
    ])
  }

  return (
    <div className="page">
      <Header />

      <main className="container main-grid">
        {/* 왼쪽: 추후 뉴스/날씨 등 다른 메인 위젯이 들어갈 자리 */}
        <section className="placeholder-card" aria-label="메인 콘텐츠 영역">
          <h2 className="placeholder-card__title">메인 콘텐츠</h2>
          <p className="placeholder-card__desc">
            이곳에 뉴스 · 날씨 · 쇼핑 등 다른 위젯을 추가할 수 있습니다.
          </p>
        </section>

        {/* 오른쪽: 블로그 기능 전용 공간 */}
        <BlogSection posts={posts} onAddPost={addPost} />
      </main>

      <footer className="footer">
        <div className="container">
          <p>© devryu — NAVER 스타일 메인 클론 (학습용)</p>
        </div>
      </footer>
    </div>
  )
}
