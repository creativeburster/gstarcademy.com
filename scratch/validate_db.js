const fs = require('fs');
const path = require('path');

try {
  const quizJsPath = path.join(__dirname, '../quiz.js');
  let content = fs.readFileSync(quizJsPath, 'utf8');

  // 提取 QUIZ_DATABASE 的内容
  // 找到 const QUIZ_DATABASE = 
  const dbStartIdx = content.indexOf('const QUIZ_DATABASE =');
  if (dbStartIdx === -1) {
    throw new Error('Could not find QUIZ_DATABASE in quiz.js');
  }

  // 寻找匹配的闭合括号，或者直接通过 mock 环境运行
  // 让我们采用 mock 环境加载方案，在全局注入 DOM mock
  global.window = {
    location: { search: '' },
    addEventListener: () => {}
  };
  global.document = {
    getElementById: () => ({
      style: {},
      addEventListener: () => {},
      querySelectorAll: () => [],
      classList: { remove: () => {}, add: () => {} }
    }),
    createElement: () => ({
      style: {},
      addEventListener: () => {},
      classList: { remove: () => {}, add: () => {} }
    }),
    addEventListener: () => {}
  };
  global.localStorage = {
    getItem: () => null,
    setItem: () => {}
  };
  global.URLSearchParams = class {
    get() { return null; }
  };

  // 修改 quiz.js 内容，在最末尾加上 exports 方便我们读取
  // 我们可以通过 eval 运行它，但把最后的 init() 调用 mock 掉
  // 把 init() 改成空函数或者在全局 mock
  global.init = () => {};
  
  // 剥离 IIFE 外壳以获取其中的局部变量，或者简单地用 eval 替换末尾的 init(); 
  // 让我们把 "init();" 替换成 "global.QUIZ_DATABASE_EXPORT = QUIZ_DATABASE;"
  let evalContent = content.replace('init();', 'global.QUIZ_DATABASE_EXPORT = QUIZ_DATABASE;');
  
  // 执行代码
  eval(evalContent);

  const db = global.QUIZ_DATABASE_EXPORT;
  if (!db) {
    throw new Error('Failed to export QUIZ_DATABASE');
  }

  console.log('✅ Successfully loaded QUIZ_DATABASE. Starting validation...');

  const tracks = ['bim', 'mcad', 'civil', 'draft'];
  
  tracks.forEach(trackKey => {
    const track = db[trackKey];
    if (!track) {
      throw new Error(`Track ${trackKey} is missing!`);
    }
    
    console.log(`\nAnalyzing Track: ${track.trackTitle} (${track.trackBadge})`);
    
    // Check nodesToMaster
    if (!Array.isArray(track.nodesToMaster) || track.nodesToMaster.length !== 5) {
      throw new Error(`Track ${trackKey} must have exactly 5 nodesToMaster, got: ${track.nodesToMaster ? track.nodesToMaster.length : 0}`);
    }
    console.log(`- nodesToMaster: [${track.nodesToMaster.join(', ')}]`);
    
    // Check lessons
    if (!Array.isArray(track.lessons) || track.lessons.length !== 3) {
      throw new Error(`Track ${trackKey} must have exactly 3 lessons, got: ${track.lessons ? track.lessons.length : 0}`);
    }
    
    let totalQuestions = 0;
    
    track.lessons.forEach((lesson, index) => {
      const expectedId = index + 1;
      if (lesson.id !== expectedId) {
        throw new Error(`Track ${trackKey} Lesson index ${index} has wrong id: ${lesson.id}, expected: ${expectedId}`);
      }
      
      if (!lesson.title || !lesson.desc) {
        throw new Error(`Track ${trackKey} Lesson ${lesson.id} is missing title or desc!`);
      }
      
      if (!Array.isArray(lesson.questions) || lesson.questions.length < 2) {
        throw new Error(`Track ${trackKey} Lesson ${lesson.id} must have at least 2 questions, got: ${lesson.questions ? lesson.questions.length : 0}`);
      }
      
      console.log(`  - Lesson ${lesson.id}: "${lesson.title}" (${lesson.questions.length} questions)`);
      
      lesson.questions.forEach((q, qIdx) => {
        totalQuestions++;
        
        if (!q.nodeId || !q.slug || !q.question || !Array.isArray(q.options) || typeof q.correctIdx !== 'number' || !q.why || !q.pitfall) {
          throw new Error(`Track ${trackKey} Lesson ${lesson.id} Q${qIdx + 1} has missing or malformed fields!`);
        }
        
        if (q.correctIdx < 0 || q.correctIdx >= q.options.length) {
          throw new Error(`Track ${trackKey} Lesson ${lesson.id} Q${qIdx + 1} has invalid correctIdx: ${q.correctIdx}`);
        }
      });
    });
    
    console.log(`- Total questions in ${trackKey}: ${totalQuestions}`);
  });
  
  // Validate Placement
  const placement = db.placement;
  if (!placement) {
    throw new Error('Placement track is missing!');
  }
  
  console.log(`\nAnalyzing Track: ${placement.trackTitle} (${placement.trackBadge})`);
  if (placement.drawCount !== 10) {
    throw new Error(`Placement must draw 10 questions, got: ${placement.drawCount}`);
  }
  if (!Array.isArray(placement.questions) || placement.questions.length !== 10) {
    throw new Error(`Placement must contain exactly 10 questions, got: ${placement.questions ? placement.questions.length : 0}`);
  }
  
  placement.questions.forEach((q, qIdx) => {
    if (!q.nodeId || !q.slug || !q.question || !Array.isArray(q.options) || typeof q.correctIdx !== 'number' || !q.why || !q.pitfall) {
      throw new Error(`Placement Q${qIdx + 1} has missing or malformed fields!`);
    }
    if (q.correctIdx < 0 || q.correctIdx >= q.options.length) {
      throw new Error(`Placement Q${qIdx + 1} has invalid correctIdx: ${q.correctIdx}`);
    }
  });
  console.log(`- Total questions in placement: ${placement.questions.length}`);

  console.log('\n🎉 ALL VALIDATIONS PASSED SUCCESSFULLY! The data structure is 100% sound.');

} catch (err) {
  console.error('\n❌ VALIDATION FAILED!');
  console.error(err);
  process.exit(1);
}
